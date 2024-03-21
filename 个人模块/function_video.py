"""
更新日期：
2023.11.21

功能：
视频的方法
"""
import os

import moviepy.editor
from PIL import Image


def get_video_info(video_file: str) -> dict:
    """获取视频的基本信息
    :param video_file: str，视频文件路径
    :return:dict，包含视频信息的字典"""
    video = moviepy.editor.VideoFileClip(video_file)

    info_filepath = video_file  # 提取文件路径
    info_filename = os.path.basename(os.path.splitext(video_file)[0])  # 提取文件名
    info_filesize = round(os.path.getsize(video_file) / 1024, 2)  # 提取文件大小/KB
    info_length = video.duration  # 提取视频时长/秒
    info_fps = round(video.fps, 2)  # 提取视频帧率
    info_kbps = round(info_filesize * 8 / info_length, 2)  # 计算视频码率
    info_width = video.w  # 提取视频宽度
    info_height = video.h  # 提取视频高度

    # 截取缩略图
    preview_numpy = video.get_frame(1)  # 截取第1秒，注意：moviepy截取的是numpy.ndarray格式
    # 将numpy.ndarray格式保存为本地图片
    preview_image = Image.fromarray(preview_numpy)
    preview_path = rf'{info_filename}.jpg'
    preview_image.save(preview_path)

    # 关闭VideoFileClip对象
    video.close()

    # 使用字典存储信息
    video_info_dict = {'info_filepath': info_filepath,
                       'info_filename': info_filename,
                       'info_filesize': info_filesize,
                       'info_fps': info_fps,
                       'info_kbps': info_kbps,
                       'info_length': info_length,
                       'info_width': info_width,
                       'info_height': info_height
                       }

    return video_info_dict
