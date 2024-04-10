import matplotlib.pyplot as plt
import struct
import math

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
                row.append((b, g, r))  # BMP 파일은 BGR 순서입니다.
            data.append(row)
    return data

#bmp배열화
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

            # HSI 데이터 저장
            hsi_row.append([h, saturation, intensity])  # Placeholder for H and S
            intensity_row.append(intensity)
        # 한 횡을 한 열에 저장
        hsi_data.append(hsi_row)
        intensity_data.append(intensity_row)

    return hsi_data, intensity_data

#intensity 값 평균화 함수
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
            Result_arr[i][j] = Result_arr[i][j] / 255.0

    return Result_arr

#intensity 바꿔치기
def changeIntensity(original_hsi, intensity_data):
    changed_hsi = []
    for i in range(height):
        changed_row = []
        for j in range(width):
            h, s, _ = original_hsi[i][j]
            changed_row.append([h, s, intensity_data[i][j]])  
        changed_hsi.append(changed_row)
    return changed_hsi         

#HSI를 rgb로
def hsiToRgb(im):
    rgb_i = [[[0, 0, 0] for _ in range(256)] for _ in range(256)]

    for i in range(256):
        for j in range(256):
            hue = im[i][j][0] 
            saturation = im[i][j][1] 
            intensity = im[i][j][2] 
            r, g, b = 0, 0, 0           

            chroma = (1 - abs(2 * intensity - 1)) * saturation

            # 색상 각도를 기준으로 색상 섹터를 계산
            hue_rad = math.radians(hue)
            hue_sector = hue_rad / (math.pi / 3)

            # RGB 변환에 필요한 중간값을 계산
            x = chroma * (1 - abs(hue_sector % 2 - 1))
            m = intensity - chroma / 2

            if 0 <= hue < 60:
                r, g, b = chroma, x, 0
            elif 60 <= hue < 120:
                r, g, b = x, chroma, 0
            elif 120 <= hue < 180:
                r, g, b = 0, chroma, x
            elif 180 <= hue < 240:
                r, g, b = 0, x, chroma
            elif 240 <= hue < 300:
                r, g, b = x, 0, chroma
            elif 300 <= hue < 360:
                r, g, b = chroma, 0, x

            # Ensure RGB values are within [0, 1]
            r = max(min((r + m), 1), 0)
            g = max(min((g + m), 1), 0)
            b = max(min((b + m), 1), 0)

            # Assign RGB values to the corresponding pixel (assuming rgb_i is properly defined)
            rgb_i[i][j][0] = int(r * 255) 
            rgb_i[i][j][1] = int(g * 255)
            rgb_i[i][j][2] = int(b * 255)
            
    return rgb_i

#2차원 배열을 다시 실수화하는 작업(그래프 출력을 위해서)
def graphDEF(ARR):
    arr = []
    for i in range(256):
        arr_r = []
        for j in range(256):
            #intensity 정수화
            arr_r.append(ARR[i][j] * 255)
        arr.append(arr_r)
    return arr

image_data = readBmp("i.bmp")
hsi_data, intensity_data = bmpToArray(image_data)
Equalizated_intensity_data = intensityEqualization(intensity_data)
output_hsi = changeIntensity(hsi_data, Equalizated_intensity_data)

# 출력
plt.figure(figsize=(15, 5))

# 입력 이미지 출력
plt.subplot(2, 3, 1)
plt.imshow(hsiToRgb(hsi_data))
plt.title('Input Image')

# 결과 이미지 출력
plt.subplot(2, 3, 4)
plt.imshow(hsiToRgb(output_hsi))
plt.title('Output Image')

# 입력 이미지의 히스토그램
plt.subplot(2, 3, 2)
plt.hist([pixel for row in intensity_data for pixel in row], bins=256, color='blue', alpha=0.7)
plt.title('Input Image Histogram')
plt.xlabel('Intensity')
plt.ylabel('Frequency')

# 출력 이미지의 히스토그램
plt.subplot(2, 3, 5)
plt.hist([pixel for row in graphDEF(Equalizated_intensity_data) for pixel in row], bins=256, color='red', alpha=0.7)
plt.title('Output Image Histogram')
plt.xlabel('Intensity')
plt.ylabel('Frequency')

plt.subplot(2, 3, 3)
hist_input, bins_input, _ = plt.hist([pixel for row in intensity_data for pixel in row], bins=256, color='blue', alpha=0.7, density=True, cumulative=True, histtype='step')
plt.title('Input Image Cumulative Probability')
plt.xlabel('Intensity')
plt.ylabel('Cumulative Probability')

# 출력 이미지의 히스토그램 및 누적분포 함수
plt.subplot(2, 3, 6)
hist_output, bins_output, _ = plt.hist([pixel for row in graphDEF(Equalizated_intensity_data) for pixel in row], bins=256, color='red', alpha=0.7, density=True, cumulative=True, histtype='step')
plt.title('Output Image Cumulative Probability')
plt.xlabel('Intensity')
plt.ylabel('Cumulative Probability')

plt.tight_layout() 
plt.show()