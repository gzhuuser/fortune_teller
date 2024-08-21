import cv2
import numpy as np

# 读取图像
img = cv2.imread("./myhand.png", -1)

# 设定固定高度
fixed_height = 600

# 计算缩放比例
scale_ratio = fixed_height / img.shape[0]  # 固定高度除以图像原始高度

# 计算新的宽度
new_width = int(img.shape[1] * scale_ratio)

# 按比例缩放图像
img = cv2.resize(img, (new_width, fixed_height))

# img = cv2.resize(img, (0, 0), None,0.2,0.2)  # 由于原图太大，所以压缩一下图像

# 将图像从BGR转换到HSV颜色空间
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 定义手掌的颜色范围（需要根据你的手掌颜色进行调整）
lower_skin = np.array([0, 30, 60])  # HSV中的低阈值
upper_skin = np.array([20, 150, 255])  # HSV中的高阈值

# 基于颜色范围的掩码
mask = cv2.inRange(img_hsv, lower_skin, upper_skin)

# 对掩码进行形态学操作以去除噪声
kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

# 应用掩码提取手掌区域
hand_extracted = cv2.bitwise_and(img, img, mask=mask)

# 显示原图和提取结果
# cv2.imshow("Original Image", img)
cv2.imshow("Hand Extracted", hand_extracted)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 如果需要保存结果
# cv2.imwrite('hand_extracted_color.png', hand_extracted)

'''
图像灰度化
'''
img_gray = cv2.cvtColor(hand_extracted, cv2.COLOR_RGB2GRAY)
# cv2.imshow("img_gray", img_gray)
cv2.waitKey()

'''
增加图像对比度
'''
scal = 1.7
o = img_gray * float(scal)
o[o>255] = 255
o = np.round(o)
o = o.astype(np.uint8)
img_par = np.hstack((img_gray, o))
# cv2.imshow("img_par", img_par)
cv2.waitKey()

'''
边缘检测Laplacian
'''
img_Laplacian = cv2.Laplacian(o, cv2.CV_8U, o, ksize = 5)
cv2.imshow('img_Laplacian', img_Laplacian)
cv2.waitKey()
cv2.imwrite('img_Laplacian.png', img_Laplacian)


'''
开运算
'''
# kernel = np.ones((2,2), np.uint8)
# erosio1 = cv2.erode(img_Laplacian, kernel, iterations = 1)
# dilate1 = cv2.dilate(erosio1, kernel, iterations = 1)
# res = np.hstack((erosio1,dilate1))
# cv2.imshow("res", res)
# cv2.waitKey()
'''
滤波
'''
# img_final = cv2.bilateralFilter(dilate1, 150, 80, 80)
# cv2.imshow('img_final', img_final)
# cv2.waitKey()
# cv2.destroyAllWindows()
