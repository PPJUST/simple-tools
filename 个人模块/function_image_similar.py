"""
更新日期：
2024.03.21

功能：
计算图片哈希以及相似图片的方法
"""

from typing import Union

import imagehash
import numpy
from PIL import Image

from function_image import image_to_numpy


def calc_image_hash(image_path: str, mode_hash: str) -> Union[None, str]:
    """计算图片的哈希值
    :param image_path: str, 图片路径
    :param mode_hash: str，需要计算的哈希值，ahash/phash/dhash
    :return: 二进制字符串哈希值或None"""
    image_pil = Image.open(image_path)
    if mode_hash == 'ahash':
        calc_hash = imagehash.average_hash(image_pil)  # 均值哈希
    elif mode_hash == 'phash':
        calc_hash = imagehash.phash(image_pil)  # 感知哈希
    elif mode_hash == 'dhash':
        calc_hash = imagehash.dhash(image_pil)  # 差异哈希
    else:
        calc_hash = None

    # 转为01二进制字符串，方便存储和读取
    if calc_hash:
        calc_hash_str = numpy_hash_to_str(calc_hash)
    else:
        calc_hash_str = None

    return calc_hash_str


def numpy_hash_to_str(hash_numpy) -> Union[str, None]:
    """将哈希值的numpy数组(imagehash.hash对象)转换为二进制字符串"""
    if not hash_numpy:
        return None
    if type(hash_numpy) is imagehash.ImageHash:
        hash_numpy = hash_numpy.hash

    hash_str = ''
    for row in hash_numpy:
        for col in row:
            if col:
                hash_str += '1'
            else:
                hash_str += '0'

    return hash_str


def calc_images_ssim(image_1, image_2) -> float:
    """计算两张图片的SSIM相似度
    :param image_1: 图片1路径
    :param image_2: 图片2路径
    :return: float，图片相似度0~1"""
    image_1_numpy = image_to_numpy(image_1, gray=True, resize=(8, 8))
    image_2_numpy = image_to_numpy(image_2, gray=True, resize=(8, 8))

    # 计算均值、方差和协方差
    mean1, mean2 = numpy.mean(image_1_numpy), numpy.mean(image_2_numpy)
    var1, var2 = numpy.var(image_1_numpy), numpy.var(image_2_numpy)
    covar = numpy.cov(image_1_numpy.flatten(), image_2_numpy.flatten())[0][1]

    # 设置常数
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    # 计算SSIM
    numerator = (2 * mean1 * mean2 + c1) * (2 * covar + c2)
    denominator = (mean1 ** 2 + mean2 ** 2 + c1) * (var1 + var2 + c2)
    ssim = numerator / denominator

    return ssim


def calc_hamming_distance(hash_str1: str, hash_str2: str) -> int:
    """计算两个二进制字符串哈希值的汉明距离
    :return: int，汉明距离"""
    hamming_distance = sum(ch1 != ch2 for ch1, ch2 in zip(hash_str1, hash_str2))

    return hamming_distance


def calc_two_hash_str_similar(hash_str1, hash_str2) -> float:
    """计算两个二进制字符串哈希值的相似度
    :return: float，图片相似度0~1"""
    hamming_distance = calc_hamming_distance(hash_str1, hash_str2)
    similarity = 1 - hamming_distance / len(hash_str1)

    return similarity
