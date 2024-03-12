import logging
from concurrent import futures

import cv2
import grpc
import numpy as np

import captcha_pb2
import captcha_pb2_grpc

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(filename)s:%(lineno)d] : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


class CaptchaProcessingServicer(captcha_pb2_grpc.CaptchaProcessingServicer):

    def ProcessCaptcha(self, request, context):
        bg_path = request.bg_path
        front_path = request.front_path

        result = []

        # 加载图像，包含透明通道
        bg = cv2.imread(bg_path)
        front = cv2.imread(front_path, cv2.IMREAD_UNCHANGED)

        # 创建与图像尺寸相同的白色背景图像
        white_front = np.ones_like(front) * 255

        # 提取图像的透明度通道
        alpha_channel = front[:, :, 3]

        # 将透明部分的像素值设置为白色
        white_front[:, :, 0:3] = cv2.bitwise_and(
            white_front[:, :, 0:3],
            white_front[:, :, 0:3],
            mask=cv2.bitwise_not(alpha_channel)
        )

        # 提取矩形区域
        rectangle_list = [[9, 9, 75, 75], [109, 9, 175, 75], [209, 9, 275, 75]]
        for rectangle in rectangle_list:
            cropped_image = white_front[rectangle[1]:rectangle[3], rectangle[0]:rectangle[2]]

            res = cv2.matchTemplate(
                cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY),
                cv2.bitwise_not(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)),
                cv2.TM_CCOEFF_NORMED
            )
            x, y = cv2.minMaxLoc(res)[3]
            result.append(captcha_pb2.Result(x=x + 20, y=y + 20))

        logging.info(f"Done process: "+str(result).replace('\n', ' '))
        return captcha_pb2.ResultResponse(results=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    captcha_pb2_grpc.add_CaptchaProcessingServicer_to_server(CaptchaProcessingServicer(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("Starting server")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
