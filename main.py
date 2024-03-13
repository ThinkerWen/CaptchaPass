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
        result = []
        bg_path = request.bg_path
        front_path = request.front_path

        """
        加载图像
        背景为jpg格式的普通图像 像素为 765x396
        目标为png格式的包含透明通道图像 像素为 300x84
        """
        bg = cv2.imread(bg_path)
        front = cv2.imread(front_path, cv2.IMREAD_UNCHANGED)

        """
        由于目标图为透明黑色图片，直接加载会导致图像全黑，
        为了避免全黑情况，创建与图像尺寸相同的白色背景图像，再提取图像的透明度通道，将透明部分的像素值设置为白色
        这样加载完后的图像就变成了白底黑色目标的图像
        """
        white_front = np.ones_like(front) * 255
        alpha_channel = front[:, :, 3]
        white_front[:, :, 0:3] = cv2.bitwise_and(
            white_front[:, :, 0:3],
            white_front[:, :, 0:3],
            mask=cv2.bitwise_not(alpha_channel)
        )

        """
        为了按序点击，需要提取目标区域的矩形方块
        由于目标图像较为规律有序，于是计算出3个目标图像像素坐标，直接按像素截取
        """
        rectangle_list = [[9, 9, 75, 75], [109, 9, 175, 75], [209, 9, 275, 75]]
        for rectangle in rectangle_list:
            cropped_image = white_front[rectangle[1]:rectangle[3], rectangle[0]:rectangle[2]]

            """
            将背景图片转换为黑白两色的图片，只保留RGB(250-255)的图像
            如此能保留绝大部分目标图像轮廓
            
            将目标图像转换为黑色背景白色轮廓
            如此便与背景的颜色逻辑一致
            """
            gray_bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
            _, strong_contrast_bg = cv2.threshold(gray_bg, 250, 255, cv2.THRESH_BINARY)
            strong_contrast_front = cv2.bitwise_not(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY))

            res = cv2.matchTemplate(
                strong_contrast_bg,
                strong_contrast_front,
                cv2.TM_CCOEFF_NORMED
            )
            """
            使用 TM_CCOEFF_NORMED 算法匹配到最佳
            由于此时的 X,Y 坐标为左上角坐标，需要加20进行偏移处理，获取到点击坐标
            """
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
