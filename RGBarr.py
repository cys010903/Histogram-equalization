import matplotlib.pyplot as plt
import struct
import math
import numpy as np

height, width= 256, 256
#bmp불러오기
def readBmp(file_path):
    # BMP 파일을 읽어들입니다.
    with open(file_path, 'rb') as f:
        # 파일 헤더를 읽습니다.
        header = f.read(54)  # BMP 파일 헤더는 보통 54바이트입니다.

        # 이미지 너비와 높이를 추출합니다.
        width = struct.unpack('<i', header[18:22])[0]
        height = struct.unpack('<i', header[22:26])[0]

        # 이미지 데이터를 읽어들입니다.
        data = []
        for _ in range(height):
            row = []
            for _ in range(width):
                b, g, r = struct.unpack('<BBB', f.read(3))
                row.append((r, g, b))  # BMP 파일은 BGR 순서입니다.
            data.append(row)

    return data
#bmp픽셀화하기
def bmpToArray(pixel_data):
    # 픽셀 데이터를 3차원 배열로 변환 (HSI)
    hsi_data = []
    intensity_data = []
    for i in reversed(range(height)):
        hsi_row = []
        intensity_row = []
        for j in range(width):
            # BGR 순서로 변환
            b = pixel_data[i][j][0] / 255.0
            g = pixel_data[i][j][1] / 255.0
            r = pixel_data[i][j][2] / 255.0
            
            #print(f"Pixel ({i}, {j}): R={r*255}, G={g*255}, B={b*255}")  # Debug print

            # Intensity 계산
            intensity = (r + g + b) / 3
             
            cmin = min(r, g, b)
            if (r + g + b) == 0:
                saturation = 0
            else:
                saturation = 1 - cmin / intensity

            # Hue 계산
            if saturation == 0:
                h = 0
            else:
                denominator = ((r - g) * (r - g) + (r - b) * (g - b))
                if denominator == 0:
                    h = 0
                else:
                    theta = math.acos((0.5 * ((r - g) + (r - b))) /
                                      math.sqrt((r - g)**2 + (r - b) * (g - b)))
                    if b > g:
                        h = 360 - math.degrees(theta)
                    else:
                        h = math.degrees(theta)

            
            #print(f"I: {intensity}, h:{h}, s:{saturation}")  # Debug print

            # HSI 데이터 저장
            hsi_row.append([h, saturation, intensity])  # Placeholder for H and S
            intensity_row.append(intensity)
        # 한 횡을 한 열에 저장
        hsi_data.append(hsi_row)
        intensity_data.append(intensity_row)

    return hsi_data, intensity_data
# intensity 값 평균화 함수
def intensityEqualization(rgb_arr):
    # intensity 배열 중 하나
    k =  0
    b_sum = 0
    total_pixels = 256*256
    Result_arr = [[0 for _ in range(256)] for _ in range(256)]
    hist = [0] * 256
    sum_of_hist = [0] * 256
    #각 픽셀 값에 대한 히스토그램 값 처리
    for i in range(256):
        for j in range(256):
            #intensity 정수화
            rgb_arr[i][j] = int(rgb_arr[i][j] * 255)
            k = rgb_arr[i][j]
            hist[k] += 1
    #누적 히스토그램 계산
    for i in range(256):
        b_sum = 0
        for j in range(i+1):
            b_sum += hist[j]
        sum_of_hist[i] = b_sum
    # 히스토그램 평활화 적용
    for i in range(256):
        for j in range(256):
            k = rgb_arr[i][j]
            Result_arr[i][j] = sum_of_hist[k] * (255 / total_pixels)
            #반환되는 intensity 다시 실수화
            Result_arr[i][j] / 255.0
    
    return Result_arr
#HSI바꿔치기
def changeIntensity(original_i, changed_intensity):
    for i in range(height):
        for j in range(width):
            original_i[i][j][2] = changed_intensity[i][j]  
    return original_i         

#HSI를 rgb로
def hsiToRgb(im):
    rgb_i = [[[0, 0, 0] for _ in range(256)] for _ in range(256)]

    for i in range(256):
        for j in range(256):
            hue = im[i][j][0] 
            saturation = im[i][j][1] 
            intensity = im[i][j][2] 
            
            print(f"I: {intensity}, h:{hue}, s:{saturation}")  # Debug print
            
            # 색조 각도를 도에서 라디안으로 변환
            hue_rad = math.radians(hue)

            # 채도와 강도를 사용하여 채도를 계산
            chroma = (1 - abs(2 * intensity - 1)) * saturation

            # 색상 각도를 기준으로 색상 섹터를 계산
            hue_sector = hue_rad / (math.pi / 3)

            # RGB 변환에 필요한 중간값을 계산
            x = chroma * (1 - abs(hue_sector % 2 - 1))
            m = intensity - chroma / 2

            r, g, b = 0, 0, 0

            if 0 <= hue_sector < 1:
                r, g, b = chroma, x, 0
            elif 1 <= hue_sector < 2:
                r, g, b = x, chroma, 0
            elif 2 <= hue_sector < 3:
                r, g, b = 0, chroma, x
            elif 3 <= hue_sector < 4:
                r, g, b = 0, x, chroma
            elif 4 <= hue_sector < 5:
                r, g, b = x, 0, chroma
            elif 5 <= hue_sector < 6:
                r, g, b = chroma, 0, x

            # 8비트 정수로 변환.

            # Assign RGB values to the corresponding pixel
            rgb_i[i][j][0] = r
            rgb_i[i][j][1] = g
            rgb_i[i][j][2] = b
            
            print(f"Pixel ({i}, {j}): R={r*255}, G={g*255}, B={b*255}")  # Debug print
            
    return rgb_i

image_data = readBmp("i.bmp")
hsi_data, intensity_data = bmpToArray(image_data)
hsiToRgb(hsi_data)

#출력
plt.figure(figsize=(10, 5))
#이미지 출력
plt.subplot(1, 2, 1)
plt.imshow(hsiToRgb(hsi_data))
plt.title('Input Image')
#결과 이미지 출력
plt.subplot(1, 2, 2)
plt.title('Output Image')

plt.tight_layout() 
plt.show()

