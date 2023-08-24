# convert pdf to jpg
import matplotlib.pyplot as plt
import matplotlib.image as img
import os
import numpy as np
import time
from pdf2image import convert_from_path # 如果要使用 convert_from_path 的話，需要下載 poppler 到同個資料夾
import cv2
import keras_ocr
import math
from inpaint_text import *
from extract_image_from_pdf import *
from image_display_and_save import *
from convert_pdf_to_jpg import *
from get_bounding_box import *


# 記錄開始時間
start_time = time.time()

# 獲取 raw data
#raw_image = convert_pdf_to_jpg_windows_os("data/pdf/1_pic.pdf", "poppler-23.08.0/Library/bin")
raw_images = convert_pdf_to_jpg_linux_os("data/pdf/1_pic.pdf")

# 將文字抹除
inpainted_texts_imgs = inpaint_texts(raw_images)

# 獲取 bb 資訊
image, bb_infos = get_image_bb( inpainted_texts_imgs[0],
                                binary_threshold=70,
                                bounding_box_size=(50,50))

# 過濾 bb
filtered_bb_infos = get_filter_bb(bb_infos)

masked_image = mask_outside_bounding_box(raw_images[0], filtered_bb_infos[0])

# 轉換圖片到灰階
gray_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)

# 二值化
ret, gray = cv2.threshold(gray_image, 70, 255, cv2.THRESH_BINARY)     # 如果大於 127 就等於 255，反之等於 0。

# 使用Canny進行邊緣檢測
edges = cv2.Canny(gray, 20, 30)  # 這裡的100和200是閾值，你可以根據需要進行

# 獲取 bb 資訊
image, bb_infos = get_image_bb( edges,
                                binary_threshold=70,
                                bounding_box_size=(50,50))

# 過濾 bb
filtered_bb_infos = get_filter_bb(bb_infos)

masked_image = mask_outside_bounding_box(raw_images[0], filtered_bb_infos[0])

# 儲存圖片
cv2.imwrite('edge_image.jpg', masked_image)






# 記錄結束時間
end_time = time.time()
# 計算並打印所需時間
elapsed_time = end_time - start_time
print(f"The function took {elapsed_time:.2f} seconds to complete.")