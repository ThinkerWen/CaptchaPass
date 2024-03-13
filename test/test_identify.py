import os.path

import cv2
import numpy as np


def show(name):
    cv2.imshow('Show', name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process(bg_path: str, front_path: str) -> None:
    bg = cv2.imread(bg_path)
    front = cv2.imread(front_path, cv2.IMREAD_UNCHANGED)

    white_front = np.ones_like(front) * 255
    alpha_channel = front[:, :, 3]
    white_front[:, :, 0:3] = cv2.bitwise_and(
        white_front[:, :, 0:3],
        white_front[:, :, 0:3],
        mask=cv2.bitwise_not(alpha_channel)
    )

    rectangle_list = [[9, 9, 75, 75], [109, 9, 175, 75], [209, 9, 275, 75]]
    for idx, rectangle in enumerate(rectangle_list, start=1):
        cropped_image = white_front[rectangle[1]:rectangle[3], rectangle[0]:rectangle[2]]

        gray_bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
        _, strong_contrast_bg = cv2.threshold(gray_bg, 250, 255, cv2.THRESH_BINARY)

        res = cv2.matchTemplate(
            strong_contrast_bg,
            cv2.bitwise_not(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)),
            cv2.TM_CCOEFF_NORMED
        )
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        x, y = max_loc
        x, y = x + 20, y + 20
        cv2.putText(bg, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (7, 249, 151), 2)
    show(bg)


if __name__ == '__main__':
    for i in range(0, 5):
        process(
            os.path.join(os.getcwd(), f"images/bg{i}.jpg"),
            os.path.join(os.getcwd(), f"images/front{i}.png")
        )
