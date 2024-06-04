"""
更新日期：
...

功能：
文件的方法
"""
import ctypes
import os
import random
import shutil
import string
import time
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
    get_file_attributes_w = ctypes.windll.kernel32.GetFileAttributesW
    file_attribute_hidden = 0x2
    invalid_file_attributes = -1

    def is_hidden(file):
        # 获取文件属性
        attrs = get_file_attributes_w(file)
        if attrs == invalid_file_attributes:
            # 文件不存在或无法访问
            return False

        return attrs & file_attribute_hidden == file_attribute_hidden

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


def get_first_multi_path(dirpath: str) -> str:
    """检查传入文件夹路径的层级，找出首个含多文件的文件夹路径或单文件路径
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
            return get_first_multi_path(check_path)
    else:
        return dirpath


def create_nodup_filename(path: str, target_dirpath: str, dup_suffix: str = ' -New',
                          target_filetitle: str = None) -> str:
    """
    生成指定路径对应的文件在目标文件夹中无重复的文件名（可指定目标文件名）
    :param path: str，文件路径或文件夹路径
    :param target_dirpath: str，目标文件夹路径
    :param dup_suffix: 若存在重复文件名则添加的后缀
    :param target_filetitle: str，目标文件名（不含后缀）
    :return: str，无重复的文件名（非完整路径，仅含后缀的文件名）
    """
    # 提取原始文件名
    dirpath = os.path.dirname(path)
    if os.path.isfile(path):
        filetitle = os.path.basename(os.path.splitext(path)[0])
        suffix = os.path.splitext(path)[1]
    else:
        filetitle = os.path.basename(path)
        suffix = ''

    # 剔除原始文件名中的自定义后缀
    index_suffix = filetitle.rfind(dup_suffix)
    if index_suffix != -1 and filetitle[index_suffix + len(dup_suffix):].isdigit():
        filetitle = filetitle[0:index_suffix]

    # 生成目标文件名
    if target_filetitle:
        new_filename = target_filetitle + suffix
        temp_filename = target_filetitle + dup_suffix + '1' + suffix
    else:
        target_filetitle = filetitle
        new_filename = filetitle + suffix
        temp_filename = filetitle + dup_suffix + '1' + suffix

    # 生成无重复的目标文件名
    # 一直循环累加直到不存在相同文件名（同级目录也要检查，防止重命名时报错）
    count = 0
    while os.path.exists(os.path.join(target_dirpath, new_filename)) or os.path.exists(
            os.path.join(dirpath, temp_filename)):
        count += 1
        new_filename = f'{target_filetitle}{dup_suffix}{count}{suffix}'
        temp_filename = new_filename

    return new_filename


def un_nested_folder(origin_folder: str, target_folder: str = None) -> str:
    """解套文件夹（将最深一级非空文件夹移动至文件夹外），并返回最终路径str
    :param origin_folder: str，原始文件夹路径
    :param target_folder: str，移动到目标文件夹，没有传参时默认移动到原始文件夹父目录
    :return: str，最终路径
    """
    # 如果传参目标文件夹且该路径不存在，则新建
    if target_folder and not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 提取最深一级的文件夹路径/如果是单文件则为该文件路径
    need_move_path = get_first_multi_path(origin_folder)

    # 检查需移动的路径和目标文件夹是否一致，如果一致，则不进行后续操作
    if need_move_path == target_folder:
        return need_move_path

    # 提取文件名，生成目标文件夹下无重复的文件/文件夹名
    final_folder = target_folder if target_folder else os.path.dirname(origin_folder)
    new_filename = create_nodup_filename(need_move_path, final_folder)

    # 如果目标路径就是原始路径，则直接返回
    if os.path.normpath(os.path.join(final_folder, new_filename)) == os.path.normpath(origin_folder):
        return origin_folder

    # 先改名
    old_path_with_new_filename = os.path.normpath(os.path.join(os.path.split(need_move_path)[0], new_filename))
    try:
        os.rename(need_move_path, old_path_with_new_filename)
    except PermissionError:  # 报错【PermissionError: [WinError 5] 拒绝访问。】，等待0.2秒再次尝试
        time.sleep(0.2)
        try:
            os.rename(need_move_path, old_path_with_new_filename)
        except PermissionError:  # 如果还存在文件占用问题，则直接移动到随机生成的文件夹中
            old_path_with_new_filename = need_move_path
            random_ascii = ''.join(random.choices(string.ascii_lowercase, k=6))
            final_folder = os.path.normpath(
                os.path.join(final_folder, os.path.basename(need_move_path) + f'_{random_ascii}'))

    # 再移动
    try:
        shutil.move(old_path_with_new_filename, final_folder)
    except OSError:  # 报错【OSError: [WinError 145] 目录不是空的。】，原始文件夹下有残留的空文件夹，尝试直接删除
        delete_empty_folder(need_move_path, to_recycle_bin=False)

    # 组合最终路径
    final_path = os.path.normpath(os.path.join(final_folder, new_filename))
    delete_empty_folder(origin_folder, to_recycle_bin=False)  # 如果原始文件夹为空，则直接删除

    return final_path


def reverse_path(path: str):
    """反转路径，从后到前排列目录层级"""
    path = os.path.normpath(path)
    split_path = path.split('\\')
    path_reversed = ' \\ '.join(split_path[::-1])
    return path_reversed
