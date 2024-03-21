"""
更新日期：
2023.11.21

功能：
一般方法
"""
import inspect
import random
import string
import time
from typing import Union


def print_function_info(mode: str = 'current'):
    """
    打印当前/上一个执行的函数信息
    :param mode: str类型，'current' 或 'last'
    """
    # pass

    if mode == 'current':
        print(time.strftime('%H:%M:%S ', time.localtime()),
              inspect.getframeinfo(inspect.currentframe().f_back).function)
    elif mode == 'last':
        print(time.strftime('%H:%M:%S ', time.localtime()),
              inspect.getframeinfo(inspect.currentframe().f_back.f_back).function)


def get_format_time(time_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取当前时间的标准化格式str
    :param time_format: str，自定义时间格式
    :return: str，标准化时间str"
    """
    return time.strftime(time_format, time.localtime())


def create_random_string(length: int = 16) -> str:
    """生成一个指定长度的随机字符串
    :param length: int，字符串长度
    :return: str，随机字符串"""
    # 小写英文 string.ascii_lowercase
    # 大写英文 string.ascii_uppercase
    # 数字 string.digits
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(characters, k=length))

    return random_string


def check_filename_feasible(filename: str, replace: bool = False) -> Union[str, bool]:
    """检查一个文件名是否符合Windows文件命名规范
    :param filename: str，仅文件名（不含路径）
    :param replace: bool，是否替换非法字符"""
    # 官方文档：文件和文件夹不能命名为“.”或“..”，也不能包含以下任何字符: \ / : * ? " < > |
    except_word = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    if not replace:  # 不替换时，仅检查
        # 检查.
        if filename[0] == '.':
            return False

        # 检查其余符号
        for key in except_word:
            if key in filename:
                return False
        return True

    else:
        for word in except_word:  # 替换符号
            filename = filename.replace(word, '')
        while filename[0] == '.':  # 替换.
            filename = filename[1:]

        return filename.strip()
