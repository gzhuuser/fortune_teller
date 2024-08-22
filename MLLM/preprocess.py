import cv2
import numpy as np


def preprocess_hand_image(image_path):
    # 读取图像
    img = cv2.imread(image_path, -1)

    # 检查图像是否读取成功
    if img is None:
        raise FileNotFoundError(f"无法打开或读取图像: {image_path}")

    # 获取图像的高度和宽度
    original_height, original_width = img.shape[:2]

    # 如果图像过大，可以考虑缩小图像，但保留其原有比例
    max_height = 1000  # 设置一个最大高度以控制处理图像的大小
    if original_height > max_height:
        scale_ratio = max_height / original_height
        new_width = int(original_width * scale_ratio)
        img = cv2.resize(img, (new_width, max_height))
    else:
        scale_ratio = 1  # 如果图像已经在最大高度以内，则保持原大小

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

    # 图像灰度化
    img_gray = cv2.cvtColor(hand_extracted, cv2.COLOR_RGB2GRAY)

    # 增加图像对比度
    scal = 1.7
    o = img_gray * float(scal)
    o[o > 255] = 255
    o = np.round(o)
    o = o.astype(np.uint8)

    # 边缘检测Laplacian
    img_Laplacian = cv2.Laplacian(o, cv2.CV_8U, o, ksize=5)

    # 将处理后的图像覆盖保存到原路径
    cv2.imwrite(image_path, img_Laplacian)
