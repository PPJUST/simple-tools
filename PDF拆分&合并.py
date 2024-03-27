import os
import sys
import tkinter.messagebox

import filetype
import fitz

try:
    drop_paths = sys.argv[1:]
except IndexError:
    drop_paths = []


def merge_pdfs(pdfs_path: list, output: str = 'output.pdf'):
    """合并多个PDF"""
    merged_pdf = fitz.open()  # 最终合并的PDF

    for child_pdf in pdfs_path:
        pdf = fitz.open(child_pdf)
        for page_num in range(pdf.page_count):
            merged_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num, start_at=merged_pdf.page_count)
        pdf.close()

    dirpath = os.path.dirname(pdfs_path[0])
    merged_pdf.save(f'{dirpath}/{output}')
    merged_pdf.close()


def split_pdf(pdf_path: str):
    """拆分PDF的每页为单独的PDF"""
    source_pdf = fitz.open(pdf_path)

    page_count = source_pdf.page_count
    if page_count == 1:
        return
    elif page_count > 1:
        filetitle = os.path.basename(os.path.splitext(pdf_path)[0])
        dirpath = os.path.dirname(pdf_path)
        os.mkdir(f'{dirpath}/{filetitle}')
        for page_num in range(source_pdf.page_count):
            single_pdf = fitz.open()
            single_pdf.insert_pdf(source_pdf, from_page=page_num, to_page=page_num)
            single_pdf.save(f'{dirpath}/{filetitle}/{page_num + 1}.pdf')
            single_pdf.close()

    source_pdf.close()


def get_files(folder: str):
    """获取文件夹下所有文件路径"""
    files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for j in filenames:
            filepath_join = os.path.normpath(os.path.join(dirpath, j))
            files.append(filepath_join)

    return files


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


def show_info():
    tkinter.Tk().withdraw()
    tkinter.messagebox.showinfo(title='使用说明',
                                message='直接将文件/文件夹拖到程序上使用。\n拖入多个PDF：合并为1个PDF\n拖入单个PDF：拆分每页为单独的PDF')


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
    pdfs = [i for i in files if is_pdf(i)]

    if len(pdfs) == 1:  # 拆分PDF
        split_pdf(pdfs[0])
    elif len(pdfs) > 1:  # 合并PDF
        merge_pdfs(pdfs)


if __name__ == '__main__':
    if drop_paths:
        main()
    else:
        show_info()
