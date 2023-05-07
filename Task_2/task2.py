import cv2
import numpy as np
from imutils import contours as cont
from collections import defaultdict
import pytesseract
from PIL import ImageFont, ImageDraw, Image
from tabula.io import read_pdf

class Line():
    def __init__(self, startx, starty, endx, endy):
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy

    def __str__(self):
        return 'Line:{},{},{},{}'.format(self.startx, self.starty, self.endx, self.endy)

    def lenx(self):
        return abs(self.startx - self.endx)

    def leny(self):
        return abs(self.starty - self.endy)

    def toArray(self):
        return [self.startx, self.starty, self.endx, self.endy]


def reDrawLine(img, aleft, aright, same_len=True):
    w, h = img.shape[0], img.shape[1]
    for r in range(w - 1):
        pixel_white = 0
        start = 0
        end = 0
        for c in range(h - 1):
            if img[r, c] == 255:
                pixel_white += 1
            if img[r, c] == 0 and img[r, c + 1] == 255:
                start = c
            if img[r, c] == 255 and img[r, c + 1] == 0:
                end = c
        if pixel_white > 20:
            if same_len:
                img[r, aleft:aright] = 255
            else:
                img[r, start:end] = 255
    return img


def findMinMaxRow(v_img):
    aleft, aright = 0, 0
    list_col = []
    w, h = v_img.shape[0], v_img.shape[1]
    for r in range(w - 1):
        pixel_white = 0
        for c in range(h - 1):
            if v_img[r, c] == 255:
                pixel_white += 1
        if pixel_white > 20:
            list_col.append(r)
    aleft, aright = min(list_col, default=0), max(list_col, default=0)
    return aleft, aright


def getLines(img):
    lines = []
    w, h = img.shape[0], img.shape[1]
    for r in range(w - 1):
        pixel_white = 0
        startx, starty, endx, endy = 0, 0, 0, 0
        for c in range(h - 1):
            if img[r, c] == 0 and img[r, c + 1] == 255:
                startx = c
                starty = r
            if img[r, c] == 255 and img[r, c + 1] == 0:
                endx = c
                endy = r
            if img[r, c] == 255:
                pixel_white += 1
        if pixel_white > 20:
            lines.append(Line(startx, starty, endx, endy))
            # print(Line(startx,starty,endx,endy).toArray())
    return lines


def findTable(arr):
    table = defaultdict(list)
    for i, b in enumerate(arr):
        if b[2] < b[3] / 2:
            continue
        table[str(b[1])].append(b)
    # print(table)
    table = [i[1] for i in table.items()]  # if len(i[1]) > 1]
    # print(([len(x) for x in table]))
    num_cols = max([len(x) for x in table])
    # print("num_cols:",num_cols)
    table = [i for i in table if len(i) == num_cols]
    # print("table rows=", len(table))
    # print("table cols=",num_cols)
    # print("table size:{}x{}".format(len(table), num_cols))
    return table


def getTable(src_img, y_start=0, min_w=10, min_h=10):
    if y_start != 0:
        src_img = src_img[y_start:, :]
    if len(src_img.shape) == 2:
        gray_img = src_img
    elif len(src_img.shape) == 3:
        gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

    thresh_img = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, -3)
    h_img = thresh_img.copy()
    v_img = thresh_img.copy()
    scale = 15

    h_size = int(h_img.shape[1] / scale)
    h_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (h_size, 1))

    h_erode_img = cv2.erode(h_img, h_structure, 1)
    h_dilate_img = cv2.dilate(h_erode_img, h_structure, 1)

    v_size = int(v_img.shape[0] / scale)
    v_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_size))
    v_erode_img = cv2.erode(v_img, v_structure, 1)
    v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)

    aleft, aright = findMinMaxRow(v_dilate_img.T)
    aleft2, aright2 = findMinMaxRow(h_dilate_img)

    h_dilate_img = reDrawLine(h_dilate_img, aleft, aright, True)

    v_dilate_img.T[aleft, aleft2:aright2] = 255
    v_dilate_img.T[aright, aleft2:aright2] = 255

    edges = cv2.Canny(h_dilate_img, 50, 150, apertureSize=3)

    # This returns an array of r and theta values 
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    mask_img = h_dilate_img + v_dilate_img
    joints_img = cv2.bitwise_and(h_dilate_img, v_dilate_img)

    convolution_kernel = np.array(
        [[0, 1, 0],
         [1, 2, 1],
         [0, 1, 0]]
    )


    contours, _ = cv2.findContours(mask_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    (contours, boundingBoxes) = cont.sort_contours(contours, method="left-to-right")
    (contours, boundingBoxes) = cont.sort_contours(contours, method="top-to-bottom")

    table = findTable([cv2.boundingRect(x) for x in contours])


    return table  # mask_img, joints_img


def getTextOfBox(img):
    return pytesseract.image_to_string(img, config='-l vie+en --oem 1 --psm 7').strip()  # .lower()


def putTextUTF8(img, text, point, fsize=10):
    fontpath = "Roboto-Regular.ttf"
    font = ImageFont.truetype(fontpath, fsize)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(point, text, font=font, fill=((0, 0, 0)))
    img = np.array(img_pil)
    return img


def getTableValue(table, img, img_ocr, fsize):

    data = []
    header = []
    for i, row in enumerate(table):
        data_row = []
        for cell in row:
            crop = img_ocr[cell[1] + 2:cell[1] + cell[3] - 2, cell[0] + 2:cell[0] + cell[2] - 2]
            # cv2.imwrite(str(i)+".png",crop)
            cell_text = getTextOfBox(crop)
            if i == 0:
                header.append(cell_text)
                cv2.rectangle(img, (cell[0], cell[1]), (cell[0] + cell[2], cell[1] + cell[3]), (0, 255, 0), -1)
            else:
                cv2.rectangle(img, (cell[0], cell[1]), (cell[0] + cell[2], cell[1] + cell[3]), (0, 255, 255), -1)
                data_row.append(cell_text)
            img = putTextUTF8(img, cell_text, (cell[0], cell[1]), fsize)
        if i == 0:
            data.append(header)
        else:
            data.append(data_row)
    return data, img


print("Detecting Table in Image .......")

in_file_img = "keppel-69.png"
in_file_pdf = "keppel-69.pdf"

img = cv2.imread(in_file_img)
img2 = img.copy()

table = getTable(img)

data = read_pdf(in_file_pdf, pages='all')
data[0].to_excel("output2.xlsx")

print("Saved to output2.xlsx")







# data, img = getTableValue(table, img, img2, 1)
# cv2.imwrite('recog.jpg', img)