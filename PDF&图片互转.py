"""
更新日期：
2024.03.27

功能：
PDF导出为图片，图片合并为一个PDF
"""
import os
import sys
import tkinter.messagebox

import filetype
import fitz

try:
    drop_paths = sys.argv[1:]
except IndexError:
    drop_paths = []


def pdf_to_image(pdf_path: str):
    """将pdf每页导出为图片"""
    doc = fitz.open(pdf_path)
    # 根据页数分别处理，如果是单页则直接导出图片，如果为多页则导出到一个文件夹中
    pages_count = doc.page_count
    filetitle = os.path.basename(os.path.splitext(pdf_path)[0])
    dirpath = os.path.dirname(pdf_path)
    if pages_count == 1:
        pix = doc[0].get_pixmap(dpi=300)
        # 使用官方的pix.save方法保存图片
        pix.save(f'{dirpath}/{filetitle}.png')
        # 使用PIL库保存图片
        # image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # image.save(f'{dirpath}/{filetitle}.png')
    elif pages_count > 1:
        os.mkdir(f'{dirpath}/{filetitle}')
        for index, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=300)
            # 使用官方的pix.save方法保存图片
            pix.save(f'{dirpath}/{filetitle}/{index}.png')
            # 使用PIL库保存图片
            # image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            # image.save(f'{dirpath}/{filetitle}/{index}.png')


def image_to_pdf(images: list, output: str = 'output.pdf'):
    """将图片合并为pdf"""
    merged_pdf = fitz.open()  # 最终合并的PDF

    for image_file in images:
        # 读取图片，转为PDF流
        img = fitz.open(image_file)
        # rect = img[0].rect  # 读取图片尺寸
        pdf_bytes = img.convert_to_pdf()
        img.close()
        # 读取PDF流，转为PDF对象
        img_page = fitz.open("pdf", pdf_bytes)
        # 插入
        merged_pdf.insert_pdf(img_page)

    dirpath = os.path.dirname(images[0])
    merged_pdf.save(f'{dirpath}/{output}')
    merged_pdf.close()


def is_image(file: str):
    """文件是否是图片"""
    return filetype.is_image(file)


def is_pdf(file: str):
    """文件是否是pdf"""
    kind = filetype.guess(file)
    if kind is None:
        return False

    guess_type = kind.extension
    if guess_type == 'pdf':
        return True
    else:
        return False


def get_files(folder: str):
    """获取文件夹下所有文件路径"""
    files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for j in filenames:
            filepath_join = os.path.normpath(os.path.join(dirpath, j))
            files.append(filepath_join)

    return files


def show_info():
    tkinter.Tk().withdraw()
    tkinter.messagebox.showinfo(title='使用说明',
                                message='直接将文件/文件夹拖到程序上使用。\n拖入图片：合并为1个PDF\n拖入PDF：导出每页为图片')


def main():
    # 收集全部文件
    files = []
    for path in drop_paths:
        if os.path.isfile(path):
            files.append(path)
        else:
            walks = get_files(path)
            files += walks

    # 按文件类型分类
    images = [i for i in files if is_image(i)]
    pdfs = [i for i in files if is_pdf(i)]

    # 如果同时存在图片和pdf，则不做处理直接退出
    if images and pdfs:
        return

    if images:  # 图片转pdf
        image_to_pdf(images)
    elif pdfs:  # pdf导出图片
        for pdf in pdfs:
            pdf_to_image(pdf)


if __name__ == '__main__':
    if drop_paths:
        main()
    else:
        show_info()
