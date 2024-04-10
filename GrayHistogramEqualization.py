import matplotlib.pyplot as plt
import struct

def read_bmp(filename):
    with open(filename, 'rb') as f:
        # 파일 헤더 읽기
        file_header = f.read(14)
        # 비트맵 데이터 오프셋 읽기
        data_offset = struct.unpack('<I', file_header[10:14])[0]
        # 이미지 데이터 읽기
        f.seek(data_offset)
        pixel_data = f.read()
    return pixel_data

def bmp_to_array(pixel_data):
    # BMP 이미지의 너비와 높이 계산
    height, width= 256, 256
    # 픽셀 데이터를 3차원 배열로 변환 (BGR 순서로 변환)
    image_array = []
    for i in reversed(range(height)):
        row = []
        for j in range(width):
            # BGR 순서로 변환
            index = (i * width + j) * 3
            if index + 2 < len(pixel_data):  # 픽셀 데이터의 길이 확인
                blue = pixel_data[index]
                green = pixel_data[index + 1]
                red = pixel_data[index + 2]
                # RGB 형태로 저장
                row.append([red, green, blue])
        image_array.append(row)
    return image_array

# 결과 출력
def rgb_to_grayscale(image_array):
    # 이미지의 높이와 너비 가져오기
    height, width= 256, 256
    # 그레이스케일 이미지를 담을 배열 생성
    grayscale_image = []
    
    # 각 픽셀의 RGB 값을 그레이스케일로 변환
    for i in range(height):
        row = []
        for j in range(width):
            # 각 픽셀의 RGB 값 가져오기
            r, g, b = image_array[i][j]
            # 그레이스케일 값 계산
            #grayscale_value = int(0.299 * r + 0.587 * g + 0.114 * b) #가중치 계산
            grayscale_value = int((r+g+b)/3)
            # 그레이스케일 이미지 배열에 할당
            row.append(grayscale_value)
        grayscale_image.append(row)
    
    return grayscale_image


# BMP 파일 읽기
pixel_data = read_bmp('i.bmp')
# BMP 데이터를 3차원 배열로 변환
image_array = bmp_to_array(pixel_data)
m_inputImg = rgb_to_grayscale(image_array)

#초기화
k = 0
bsum = 0
total_pixels = 256*256
m_ResultImg = [[0 for _ in range(256)] for _ in range(256)]
hist = [0] * 256
sum_of_hist = [0] * 256

#각 픽셀 값에 대한 히스토그램 값 처리
for i in range(256):
    for j in range(256):
        k = m_inputImg[i][j]
        hist[k] += 1

#누적 히스토그램 계산
for i in range(256):
    bsum = 0
    for j in range(i+1):
        bsum += hist[j]
    sum_of_hist[i] = bsum

# 히스토그램 평활화 적용
for i in range(256):
    for j in range(256):
        k = m_inputImg[i][j]
        m_ResultImg[i][j] = sum_of_hist[k] * (255 / total_pixels)


plt.figure(figsize=(10, 5))

# 이미지 출력
plt.subplot(2, 3, 1)
plt.imshow(m_inputImg, cmap='gray')
plt.title('Input Image')

# 히스 출력
plt.subplot(2, 3, 2)
flat_I = []
for sublist in m_inputImg:
    for item in sublist:
        flat_I.append(item)
plt.hist(flat_I, bins=range(min(flat_I), max(flat_I) + 1), color='black')
plt.title('Input Image histogram')

# 누적분포함수
plt.subplot(2, 3, 3)
plt.plot(sum_of_hist, color='black')

# 결과 이미지 출력
plt.subplot(2, 3, 4)
plt.imshow(m_ResultImg, cmap='gray')
plt.title('Output Image')

# 결과 히스 출력
plt.subplot(2, 3, 5)
flat_R = []
for sublist in m_ResultImg:
    for item in sublist:
        flat_R.append(item)
plt.hist(flat_R, bins=range(int(min(flat_R)), int(max(flat_R)) + 1), color='black')
plt.title('Output Image histogram')

# 결과 누적분포함수
plt.subplot(2, 3, 6)
# m_ResultImg의 누적분포함수를 구하는 과정
hist = [0] * 256
for i in range(256):
    for j in range(256):
        k = m_ResultImg[i][j]
        hist[int(k)] += 1
cumulative_hist = [0] * 256
cumulative_sum = 0
for i in range(256):
    cumulative_sum += hist[i]
    cumulative_hist[i] = cumulative_sum
plt.plot(cumulative_hist , color='black')


plt.tight_layout() 
plt.show()

