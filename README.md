# CaptchaPass

项目用于过 点击式图形验证码 和 滑动式验证码 的校验

## 声明

#### 点击式：

| 背景图 | 目标图 |
| :----:| :----: |
| <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/bg0.jpg" width="200" alt="背景图"/> | <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/front0.png" width="200" alt="目标图"/> |

#### 滑动式：

|                                                              背景图                                                               |                                                                目标图                                                                |
|:------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------:|
| <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/slide_bg0.png" width="200" alt="背景图"/> | <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/slide_block0.png" width="200" alt="目标图"/> |

项目非通用解决方案，如果您的问题不满足以下几点，需要做一些简单的定制（[有引导](#定制引导)）：
#### 点击式：
1. 目标图像素为 300x84
2. 目标图为黑色图标的透明背景图
3. 背景图的目标图形为白色

## 介绍
[【看雪】Python OpenCV 过点击式和滑动式图形验证码的校验](https://bbs.kanxue.com/homepage-959049.htm)

[【52破解】Python OpenCV 过点击式和滑动式图形验证码的校验](https://www.52pojie.cn/home.php?mod=space&uid=1920139)
## 定制引导

1.如果目标图像素不是 300x84，则需要修改此处代码:
```python
# 其中 [9, 9, 75, 75] 为目标图像其中一个图标的
# 左上角坐标: P1=(9,9) 和右下角坐标: P2=(75,75)
# 需要自己计算并修改
rectangle_list = [[9, 9, 75, 75], [109, 9, 175, 75], [209, 9, 275, 75]]
```

2.如果目标图不是黑色图标的透明背景图，则需要修改此处代码:
```python
# 此处将透明背景转白色，可定制为你的
white_front = np.ones_like(front) * 255
alpha_channel = front[:, :, 3]
white_front[:, :, 0:3] = cv2.bitwise_and(
    white_front[:, :, 0:3],
    white_front[:, :, 0:3],
    mask=cv2.bitwise_not(alpha_channel)
)

# 此处将颜色反转，可定制为你的
strong_contrast_front = cv2.bitwise_not(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY))
```

3.如果背景图的目标图形不是白色，则需要修改此处代码:
```python
# 此处将图片转为灰度后仅仅保留RGB 250-255的偏白色图片，可定制为你的
gray_bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
_, strong_contrast_bg = cv2.threshold(gray_bg, 250, 255, cv2.THRESH_BINARY)
```

## 缺陷
混淆度不高，或者颜色分明的图像识别都较为容易，如: 

|                                                           背景图                                                            |                                                             目标图                                                             |
|:------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------:|
| <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/bg0.jpg" width="200" alt="背景图"/> | <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/front0.png" width="200" alt="目标图"/> |
| <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/bg1.jpg" width="200" alt="背景图"/> | <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/front1.png" width="200" alt="目标图"/> |
| <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/bg2.jpg" width="200" alt="背景图"/> | <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/front2.png" width="200" alt="目标图"/> |

但颜色与待匹配的front图像相似的难以精确匹配，如:

| 背景图 | 目标图 |
| :----:| :----: |
| <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/bg0.jpg" width="200" alt="背景图"/> | <img src="https://raw.githubusercontent.com/Raptor-wxw/CaptchaPass/main/test/images/front0.png" width="200" alt="目标图"/> |