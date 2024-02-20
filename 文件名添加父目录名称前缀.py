"""
更新日期：
2024.02.20

功能：
在指定文件夹下的所有文件的文件名前添加或删除父目录前缀
"""

import os


def walk_folder(folder):
    """遍历文件夹"""
    filepaths = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for j in filenames:
            filepath_join = os.path.normpath(os.path.join(dirpath, j))
            filepaths.append(filepath_join)

    return filepaths


def rename_with_prefix(file):
    """给文件添加或删除父目录前缀"""
    parent_folder = os.path.split(file)[0]
    dirname = os.path.split(parent_folder)[1]
    prefix = f'{dirname} - '
    filename = os.path.split(file)[1]
    # 判断是添加还是删除
    if filename.startswith(prefix):
        new_filename = filename[len(prefix):]
    else:
        new_filename = prefix + filename
    new_file = os.path.join(parent_folder, new_filename)
    os.rename(file, new_file)
    print(f'已改名：{file}')


def main():
    print('输入文件夹路径，对文件夹下的所有文件的文件名进行添加/删除父目录前缀操作')
    while True:
        print('-' * 20)
        folder = input('输入文件夹路径：')
        filepaths = walk_folder(folder)
        for i in filepaths:
            rename_with_prefix(i)


if __name__ == '__main__':
    main()
