from tabula.io import read_pdf
from mmdet.apis import init_detector, inference_detector
# from mmdet.models.detectors import BaseDetector

import mmcv


import pandas as pd

data = read_pdf("keppel-69.pdf", pages='all')

# print(data[3][1])
# x = len(data)
# y = len(data[0])
# z = data[0]
# print(x)
# print(y)
# print(z)

# for i in range(0,len(data)):
#     print("I is :"+str(i))
#     for j in range(0,len(data[i])):
#         print("J is :" + str(j))
#         print(type(data[i][j]))

print(type(data[0]))

data[0].to_excel("output2.xlsx")


# print(type(data))
# df = pd.DataFrame(data)
# df.to_excel("output2.xlsx")


# config_file = "config.py"
# checkpoint_file = 'epoch_36.pth'
# model = init_detector(config_file, checkpoint_file, device='cuda:0')
#
# img = "keppel-69.png"

# result = inference_detector(model, img)

# show_result_pyplot(img, result,('Bordered', 'cell', 'Borderless'), score_thr=0.85)
# model.show_result(img,result)
