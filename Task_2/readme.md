
# Task 2

This code provides functionality to extract tables from images or PDFs. It uses OpenCV, NumPy, pytesseract, and tabula.io libraries for image processing and table extraction.

The following are the main functions in this code:

Line: A class representing a line segment in an image.

reDrawLine(img, aleft, aright, same_len=True): A function that redraws a line in an image to fill any gaps.

findMinMaxRow(v_img): A function that returns the minimum and maximum rows that contain non-white pixels in a binary image.

getLines(img): A function that extracts all the horizontal lines from an image.

findTable(arr): A function that finds a rectangular table in a list of line segments.

getTable(src_img, y_start=0, min_w=10, min_h=10): A function that extracts a table from an image or PDF.

To use this code, you can call the getTable function and pass in an image or PDF file path. You can also specify the starting row of the table, as well as the minimum width and height of the table cells. The function will return a list of lists, where each inner list represents a row of the table, and each element in the inner list represents a cell.





