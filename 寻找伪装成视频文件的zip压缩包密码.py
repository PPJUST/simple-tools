"""
更新日期：
2024.07.07

功能：
在密码字典中寻找伪装成视频文件的zip压缩包的密码（可修改后缀名后正常解压的伪装文件）
"""

import os
import sys
import time
import zipfile
from typing import Union

import pyzipper
import filetype


def _is_video_mask(file):
    """是否是伪装成视频的压缩包"""
    if not os.path.exists(file) or not os.path.isfile(file):
        return False
    try:
        with zipfile.ZipFile(file, 'r') as zf:
            zf.setpassword('fake'.encode())
            zf.testzip()
        # 如果能成功测试，但是检测出来的格式不是压缩包，则该隐写文件无密码
        if _is_archive(file):
            return False
        else:
            return True

    except Exception as e:
        # print('报错：', e)
        e = str(e)
        if 'That compression method is not supported' in e:
            return True
        else:
            return False


def _is_archive(file):
    """使用filetype库判断是否为zip压缩文件"""
    kind = filetype.guess(file)
    if kind is None:
        return False

    guess_type = kind.extension
    print('该文件类型：')
    if guess_type == 'zip':
        return True
    else:
        return False


def _test_password(zip_file, password: str):
    """测试密码"""
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.pwd = password.encode('utf-8')
            zf.testzip()
            return True
    except Exception as e:
        # print(e)
        return False


def _change_suffix_to_zip(file):
    """修改文件后缀为 'zip'"""
    temp_path = os.path.splitext(file)[0]
    new_path = temp_path + '.zip'
    os.rename(file, new_path)
    return new_path


def _add_prefix_pw(file, pw):
    """将密码添加到文件名中"""
    dirpath, filename = os.path.split(file)
    new_filename = f'密码【{pw}】' + filename
    new_path = os.path.normpath(os.path.join(dirpath, new_filename))
    os.rename(file, new_path)


def _read_passwords():
    """读取密码"""
    pw_file_path = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '密码.txt'))
    if not os.path.exists(pw_file_path):
        with open(pw_file_path, 'w', encoding='utf-8') as pf:
            pf.close()
    try:
        with open(pw_file_path, 'r', encoding='utf-8') as pf:
            passwords = pf.readlines()
            pf.close()
    except:
        with open(pw_file_path, 'r', encoding='gbk') as pf:
            passwords = pf.readlines()
            pf.close()

    passwords = [i.strip() for i in passwords if i.strip()]
    return passwords


def test_files(files: Union[list, str], passwords: Union[list, str]):
    """测试文件"""
    if isinstance(files, str):
        files = [files]
    if isinstance(passwords, str):
        passwords = [passwords]

    passwords.insert(0, '无密码')

    for file in files:
        # 首先测试其是否为伪装成视频的压缩文件（暂时只考虑zip伪装）
        print('-' * 16)
        print(f'检查:{file}')
        if _is_video_mask(file):
            print('文件为伪装后的zip压缩文件')
            # 如果是伪装文件，则修改为真实后缀名
            new_path = _change_suffix_to_zip(file)
            print('已修改文件后缀名')
            print('开始测试密码')
            # 逐个测试密码
            result = False
            for pw in passwords:
                result = _test_password(new_path, pw)
                if result:  # 找到正确密码后中断循环
                    _add_prefix_pw(new_path, pw)
                    print(f'密码为{pw}，已写入文件名')
                    break
            if not result:  # 修改回原文件名
                os.rename(new_path, file)
                print('未找到正确密码，修改回原文件名')


_passwords = _read_passwords()
print('当前密码：', ','.join(_passwords), '\n')

try:
    _files = sys.argv[1:]
except IndexError:
    _files = []

# 测试用，输入文件夹路径
path = input('输入：')
if os.path.isfile(path):
    _files = [path]
else:
    _files = [os.path.join(path, i) for i in os.listdir(path)]

if not _files:
    print('使用：请直接拖入文件到程序图标上使用')
    print("密码：将密码写入同目录下的'密码.txt'中，一个密码占一行")
    print('5s后退出')
    time.sleep(5)
    sys.exit(0)
else:
    test_files(_files, _passwords)
    print('5s后退出')
    time.sleep(5)
    sys.exit(0)
