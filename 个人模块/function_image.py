"""
更新日期：
2024.03.21

功能：
图片操作的方法
"""
from typing import Tuple

import cv2
import numpy


def image_to_numpy(image_file: str, gray=False, resize: Tuple[int, int] = None):
    """将图片转为numpy对象
    :param image_file: 图片路径
    :param gray: bool值，是否转灰度图
    :param resize: list，缩放宽高
    :return: numpy.ndarray对象，图片的numpy对象"""
    image_numpy = cv2.imdecode(numpy.fromfile(image_file, dtype=numpy.uint8), -1)

    if resize:
        image_numpy = cv2.resize(image_numpy, resize)

    if gray:
        try:
            image_numpy = cv2.cvtColor(image_numpy, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            pass

    return image_numpy
