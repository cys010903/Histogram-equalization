import cv2
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Image path to the directory")
# args = vars(ap.parse_args())
# path = args['image']

path = "i.bmp"
# 입력 받은 이미지를 불러옵니다.
src = cv2.imread(path)



# hsv 컬러 형태로 변형합니다.
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
# h, s, v로 컬러 영상을 분리 합니다. 
h, s, v = cv2.split(hsv)
# v값을 히스토그램 평활화를 합니다.
equalizedV = cv2.equalizeHist(v)
# h,s,equalizedV를 합쳐서 새로운 hsv 이미지를 만듭니다.
hsv2 = cv2.merge([h,s,equalizedV])
# 마지막으로 hsv2를 다시 BGR 형태로 변경합니다.
hsvDst = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)

# YCrCb 컬러 형태로 변환합니다.
yCrCb = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
# y, Cr, Cb로 컬러 영상을 분리 합니다.
y, Cr, Cb = cv2.split(yCrCb)
# y값을 히스토그램 평활화를 합니다.
equalizedY = cv2.equalizeHist(y)
# equalizedY, Cr, Cb를 합쳐서 새로운 yCrCb 이미지를 만듭니다.
yCrCb2 = cv2.merge([equalizedV, Cr, Cb])
# 마지막으로 yCrCb2를 다시 BGR 형태로 변경합니다.
yCrCbDst = cv2.cvtColor(yCrCb2, cv2.COLOR_YCrCb2BGR)

# src, hls, L 각각을 출력합니다.
plt.figure(figsize=(20, 20))

# 입력 이미지 출력
plt.subplot(3, 3, 1)
plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2RGB))
plt.title('Input Image')

# 결과 이미지 출력
plt.subplot(3, 3, 4)
plt.imshow(cv2.cvtColor(hsvDst, cv2.COLOR_BGR2RGB))
plt.title('Output Image')

# 입력 이미지의 히스토그램
plt.subplot(3, 3, 2)
plt.hist(src.ravel(), bins=256, color='blue', alpha=0.7)
plt.title('Input Image Histogram')

# 출력 이미지의 히스토그램
plt.subplot(3, 3, 5)
plt.hist(hsvDst.ravel(), bins=256, color='red', alpha=0.7)
plt.title('Output Image Histogram')

# 입력 이미지의 히스토그램 및 누적분포 함수
plt.subplot(3, 3, 3)
plt.hist(src.ravel(), bins=256, color='blue', alpha=0.7, density=True, cumulative=True, histtype='step')
plt.title('Input Image Histogram and CDF')
plt.xlabel('Intensity')
plt.ylabel('Cumulative Probability')

# 출력 이미지의 히스토그램 및 누적분포 함수
plt.subplot(3, 3, 6)
plt.hist(hsvDst.ravel(), bins=256, color='red', alpha=0.7, density=True, cumulative=True, histtype='step')
plt.title('Output Image Histogram and CDF')
plt.xlabel('Intensity')
plt.ylabel('Cumulative Probability')

# yCrCb 결과 이미지 출력
plt.subplot(3, 3, 7)
plt.imshow(cv2.cvtColor(yCrCbDst, cv2.COLOR_BGR2RGB))
plt.title('YCrCb Output Image')

# yCrCb 출력 이미지의 히스토그램
plt.subplot(3, 3, 8)
plt.hist(yCrCbDst.ravel(), bins=256, color='green', alpha=0.7)
plt.title('YCrCb Output Image Histogram')

# yCrCb 출력 이미지의 히스토그램 및 누적분포 함수
plt.subplot(3, 3, 9)
plt.hist(yCrCbDst.ravel(), bins=256, color='green', alpha=0.7, density=True, cumulative=True, histtype='step')
plt.title('YCrCb Output Image Histogram and CDF')
plt.xlabel('Intensity')
plt.ylabel('Cumulative Probability')

plt.tight_layout()
plt.show()
plt.tight_layout() 
plt.show()