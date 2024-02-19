"""
更新日期：
2024.02.19

功能：
重命名使用GoPro拍摄的视频文件，命名格式为 "视频编号_章节 - 原始文件名.mp4"
GoPro的视频命名规则：https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention?language=zh_CN
"""

import os
import re

"""GoPro文件名正则"""
# GH、GX一般视频（H=AVC编码，X=HEVC编码，GHzzxxxx.mp4）
pattern_GHX = r'^(G[HX])(\d{2})(\d{4})(\.mp4)$'

# GH、GX循环视频（H=AVC编码，X=HEVC编码，同一文件看YY，GHYYxxxx.mp4）
pattern_GHX_loop = r'^(G[HX])([A-Z]{2})(\d{4})(\.mp4)$'

# GOPR、GP（GOPR固定为第一个视频，如果有分段后续编号从GP开始，GP011234.mp4）
pattern_GP_top = r'^GOPR(\d{4})(\.mp4)$'
pattern_GP_volume = r'^(GP)(\d{2})(\d{4})(\.mp4)$'


def split_filename(filename: str):
    """切割文件名为[标识符、章节、文件编号]"""
    filename_split = {'origin': filename,
                      'type': None,
                      'number': None,
                      'chapter': None,
                      'suffix': None}
    # 匹配GH、GX一般视频
    match_ghx = re.match(pattern_GHX, filename)
    if match_ghx:
        filename_split['type'] = match_ghx.group(1)
        filename_split['chapter'] = match_ghx.group(2)
        filename_split['number'] = match_ghx.group(3)
        filename_split['suffix'] = match_ghx.group(4)
        return filename_split

    # 匹配GH、GX循环视频
    match_ghx_loop = re.match(pattern_GHX_loop, filename)
    if match_ghx_loop:
        filename_split['type'] = match_ghx_loop.group(1)
        filename_split['chapter'] = match_ghx_loop.group(3)
        filename_split['number'] = match_ghx_loop.group(2)
        filename_split['suffix'] = match_ghx_loop.group(4)
        return filename_split

    # 匹配GOPR
    match_gp_top = re.match(pattern_GP_top, filename)
    if match_gp_top:
        filename_split['type'] = 'GP'
        filename_split['chapter'] = '01'
        filename_split['number'] = match_gp_top.group(1)
        filename_split['suffix'] = match_gp_top.group(2)
        return filename_split

    # 匹配GP
    match_gp = re.match(pattern_GP_volume, filename)
    if match_gp:
        filename_split['type'] = match_gp.group(1)
        filename_split['chapter'] = f'{int(match_gp.group(2)) + 1:02}'
        filename_split['number'] = match_gp.group(3)
        filename_split['suffix'] = match_gp.group(4)
        return filename_split


def create_newname(filename_split: dict):
    """生成新的文件名"""
    # 格式 视频编号_章节 - 原始文件名
    number = filename_split['number']  # 视频编号
    chapter = filename_split['chapter']  # 章节
    suffix = filename_split['suffix']  # 后缀
    origin_name = filename_split['origin'].replace(suffix, '')
    newname = f'{number}_{chapter} - {origin_name}{suffix}'
    return newname


def walk_file(dirpath: str):
    filepaths = []
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        for dirpath, dirnames, filenames in os.walk(dirpath):
            for j in filenames:
                filepath_join = os.path.normpath(os.path.join(dirpath, j))
                filepaths.append(filepath_join)

    return filepaths


def main():
    dirpath = input('输入需要改名的文件夹路径：')
    filepaths = walk_file(dirpath)
    index = 0

    for file in filepaths:
        parent_folder, filename = os.path.split(file)
        filename_split = split_filename(filename)
        if filename_split:
            newname = create_newname(filename_split)
            new_file = os.path.join(parent_folder, newname)
            os.rename(file, new_file)
            index += 1
            print(f'{filename} 改名为 {newname}')
    print(f'已完成{index}个视频文件名的修改')


if __name__ == '__main__':
    while True:
        main()
