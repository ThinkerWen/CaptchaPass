import os

import cv2


def show(name):
    cv2.imshow('Show', name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def _tran_canny(image):
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.Canny(image, 50, 150)


def process(bg_path: str, front_path: str) -> None:

    # flags0是灰度模式
    image = cv2.imread(front_path, 0)
    template = cv2.imread(bg_path, 0)
    template = cv2.resize(template, (340, 191), interpolation=cv2.INTER_CUBIC)

    # 寻找最佳匹配
    res = cv2.matchTemplate(_tran_canny(image), _tran_canny(template), cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    x, y = max_loc
    w, h = image.shape[::-1]
    cv2.rectangle(template, (x, y), (x + w, y + h), (7, 249, 151), 2)
    show(template)
    # return max_loc[0]


if __name__ == '__main__':
    for i in range(0, 1):
        # 不同环境对distance的像素的计算方式可能不同
        # 可能需要进行相应的 +-*/ 操作来求出实际滑动距离
        process(
            os.path.join(os.getcwd(), f"images/slide_bg{i}.png"),
            os.path.join(os.getcwd(), f"images/slide_block{i}.png")
        )