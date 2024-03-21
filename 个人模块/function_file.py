"""
更新日期：
...

功能：
文件的方法
"""
import ctypes
import os
from typing import Tuple

import natsort
import send2trash


def delete_empty_folder(folder_path: str, to_recycle_bin: bool = True):
    """删除指定文件夹中的空文件夹（及其自身）
    :param folder_path: str，文件夹路径
    :param to_recycle_bin: bool，是否删除至回收站
    """
    all_dirpath = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        all_dirpath.append(dirpath)  # 提取所有文件夹路径

    all_dirpath.insert(0, folder_path)  # 将其自身放于首位

    if to_recycle_bin:
        for path in all_dirpath[::-1]:  # 从后往前逐级删除
            if not os.listdir(path):
                send2trash.send2trash(path)
    else:
        for path in all_dirpath[::-1]:  # 从后往前逐级删除
            if not os.listdir(path):
                os.rmdir(path)


def is_hidden_file(path: str):
    """路径对应的文件是否隐藏"""
    GetFileAttributesW = ctypes.windll.kernel32.GetFileAttributesW
    FILE_ATTRIBUTE_HIDDEN = 0x2
    INVALID_FILE_ATTRIBUTES = -1

    def is_hidden(file):
        # 获取文件属性
        attrs = GetFileAttributesW(file)
        if attrs == INVALID_FILE_ATTRIBUTES:
            # 文件不存在或无法访问
            return False

        return attrs & FILE_ATTRIBUTE_HIDDEN == FILE_ATTRIBUTE_HIDDEN

    return is_hidden(path)


def get_folder_size(folder: str) -> int:
    """获取指定文件夹的总大小/byte
    :param folder: str类型，文件夹路径
    :return: int类型，总字节大小
    """
    folder_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for item in filenames:
            filepath = os.path.join(dirpath, item)
            folder_size += os.path.getsize(filepath)

    return folder_size


def get_dirs_files(folder: str) -> Tuple[list, list]:
    """获取一个文件夹中所有的文件列表，文件夹列表
    :return: 两个list，所有文件夹列表，所有文件列表"""
    dirs = []
    files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for k in dirnames:
            dirpath_join = os.path.normpath(os.path.join(dirpath, k))
            dirs.append(dirpath_join)

        for j in filenames:
            filepath_join = os.path.normpath(os.path.join(dirpath, j))
            files.append(filepath_join)

    return dirs, files


def get_dir_structure(dirpath: str) -> list:
    """获取一个文件夹路径的内部文件结构
    :return: list，内部结构列表，结构为子文件夹及其子文件夹与内部文件"""
    dir_list = []
    file_list = []
    for filename in natsort.natsorted(os.listdir(dirpath), alg=natsort.PATH | natsort.IGNORECASE):
        fullpath = os.path.normpath(os.path.join(dirpath, filename))
        if os.path.isdir(fullpath):
            dir_list.append(fullpath)
            dir_list += get_dir_structure(fullpath)  # 递归
        else:
            file_list.append(fullpath)

    # 整合
    join_list = dir_list + file_list

    return join_list


def get_parent_paths(input_path: str) -> list:
    """获取一个路径的所有上级目录路径
    :return: list，所有上级目录列表，路径短的在前面"""
    parent_dirs = []

    while True:
        parent_dirpath, filename = os.path.split(input_path)
        if filename:
            parent_dirs.append(parent_dirpath)
        else:
            break

        input_path = parent_dirpath

    # 反转列表顺序，使得最上级目录在最前面
    parent_dirs = parent_dirs[::-1]

    return parent_dirs


def get_first_multi_folder(dirpath: str) -> str:
    """检查传入文件夹路径的层级，找出首个含多文件/文件夹的文件夹路径
    :param dirpath: str类型，文件夹路径
    :return: str类型，文件夹路径
    """
    if len(os.listdir(dirpath)) == 1:  # 如果文件夹下只有一个文件/文件夹
        check_path = os.path.normpath(os.path.join(dirpath, os.listdir(dirpath)[0]))
        # 如果是文件，则直接返回
        if os.path.isfile(check_path):
            return check_path
        # 如果是文件夹，则递归
        else:
            return get_first_multi_folder(check_path)
    else:
        return dirpath
