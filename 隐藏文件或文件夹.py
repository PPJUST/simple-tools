"""
更新日期：
2024.03.15

功能：
隐藏/显示文件/文件夹（设置隐藏属性）
"""
import os
import subprocess


def walk_path(path):
    """遍历路径，获取内部所有文件和文件夹"""
    if not os.path.exists(path):
        return []

    if os.path.isfile(path):
        return [path]
    else:
        insides = set()
        insides.add(path)
        for dirpath, dirnames, filenames in os.walk(path):
            for j in filenames:
                filepath_join = os.path.normpath(os.path.join(dirpath, j))
                insides.add(filepath_join)

            for k in dirnames:
                dirpath_join = os.path.normpath(os.path.join(dirpath, k))
                insides.add(dirpath_join)

        return insides


def main():
    print('隐藏/显示文件/文件夹（设置隐藏属性）')
    while True:
        print('-' * 50)
        path = input('输入文件/文件夹路径：')
        is_hidden = input('Y:隐藏/N:显示：').lower() == 'y'
        insides = walk_path(path)
        if is_hidden:
            for i in insides:
                subprocess.run(['attrib', '+h', i])
                print('已隐藏：', i)
        else:
            for i in insides:
                subprocess.run(['attrib', '-h', i])
                print('已显示：', i)


if __name__ == '__main__':
    main()
