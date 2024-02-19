"""
更新日期：
2024.02.19

功能：
删除某文件夹下所有文件名符合规则的文件，并删除空文件夹
"""

import os
import re

import natsort
import send2trash

RULE_FILE = '规则.txt'
METACHARACTER_REPLACE = r".\^$[]+?{}|()"
METACHARACTER_CONVERT = "*"

info = """
*** 更新日期 ***
2024.02.19

*** 功能 ***
删除某文件夹下所有文件名符合规则的文件，并删除空文件夹

*** 使用方法 ***
1.维护好匹配规则
2.输入文件夹路径
3.查看显示的预删除文件
4.执行或放弃删除任务

*** 匹配规则编写 ***
1.在"规则.txt"中编写，一个规则占一行
2.规则不需要区分大小写英文
3.支持正则表达式，在规则前添加"#re "即可
4.一般规则参照下方说明

*** 一般规则说明 ***
匹配规则参考Excel的find/search等函数的逻辑，*为通配符

*** 一般规则示例 ***
ABC：只匹配文件名为ABC的文件
ABC*：匹配文件名以ABC开头的文件
*ABC：匹配文件名以ABC结尾的文件
*ABC*：匹配文件名中有ABC的文件
*A*BC*：匹配文件名中有A和BC且BC在A后的文件
"""

info_2 = """
输入1：打开"规则.txt"
输入2：匹配时包含文件后缀
输入3：匹配时包含不包含文件后缀（默认）
"""

rules_pattern = []
is_check_suffix = False


def check_rule_file():
    """检查规则文件是否存在"""
    if not os.path.exists(RULE_FILE):
        with open(RULE_FILE, 'w', encoding='utf-8'):
            pass


def read_rules():
    """读取规则文件，并转换为正则表达式"""
    global rules_pattern
    try:
        with open(RULE_FILE, 'r', encoding='utf-8') as f:
            rules_str = f.readlines()
    except UnicodeDecodeError:
        with open(RULE_FILE, 'r') as f:
            rules_str = f.readlines()

    # 逐个检查并转换
    rules_pattern.clear()
    for rule_str in rules_str:
        rule_str = rule_str.strip('\n')
        if rule_str.startswith('#re '):  # 正则模式
            rules_pattern.append(rule_str[4:])
        else:  # 普通模式
            # 替换特殊字符
            rule_str = re.escape(rule_str)
            # 转换*通配符
            rule_str = rule_str.replace('\\*', '.*')
            # 添加正则起始和结束标志
            rule_str = '^' + rule_str + '$'
            rules_pattern.append(rule_str)

    print('当前匹配正则表达式: ', ' ; '.join(rules_pattern))


def set_suffix_check(is_checked: bool):
    """设置是否检查文件后缀"""
    global is_check_suffix
    is_check_suffix = is_checked
    print_is_suffix_check()


def print_is_suffix_check():
    """显示是否检查文件后缀"""
    if is_check_suffix:
        print('当前设置: 匹配时包含文件后缀')
    else:
        print('当前设置: 匹配时包含不包含文件后缀')


def get_all_filepath(folder: str):
    """提取文件夹下所有的文件路径"""
    filepaths = []
    if os.path.exists(folder) and os.path.isdir(folder):
        for dirpath, dirnames, filenames in os.walk(folder):
            for j in filenames:
                filepaths.append(os.path.normpath(os.path.join(dirpath, j)))

    return filepaths


def is_file_format(check_text: str):
    """检查文件名是否符合规则"""
    for rule in rules_pattern:
        if re.match(rule, check_text, flags=re.IGNORECASE):
            return True

    return False


def get_filetitle(path):
    """提取文件名（不含后缀）"""
    if os.path.isdir(path):
        return os.path.split(path)[1]
    else:
        return os.path.split(os.path.splitext(path)[0])[1]


def get_filename(path):
    """提取文件名（含后缀）"""
    return os.path.split(path)[1]


def get_parent_folder(filepaths: list):
    """提取父目录"""
    parent_folders = []
    for i in filepaths:
        parent_folders.append(os.path.split(i)[0])

    return parent_folders


def check_files_format(filepaths: list):
    """检查文件"""
    delete_paths = []
    for file in filepaths:
        if is_check_suffix:
            check_text = get_filename(file)
        else:
            check_text = get_filetitle(file)
        if is_file_format(check_text):
            delete_paths.append(file)

    delete_paths = natsort.natsorted(delete_paths, alg=natsort.ns.PATH, reverse=True)
    return delete_paths


def delete_files(files: list):
    """删除文件"""
    for file in files:
        if os.path.exists(file):
            send2trash.send2trash(file)
            print('已删除文件：', file)


def delete_empty_folders(folders: list):
    """删除空文件夹"""
    for folder in folders:
        if os.path.exists(folder) and len(os.listdir(folder)) == 0:
            send2trash.send2trash(folder)
            print('已删除空文件夹：', folder)


def show_files(files):
    """显示预删除文件"""
    print('------预删除文件：------')
    for i in files:
        print(i)
    print(f'------共{len(files)}个文件------')


def main():
    print(info)
    print('-' * 40)
    print(info_2)
    print('-' * 40)
    print_is_suffix_check()
    while True:
        print('-' * 20)
        check_rule_file()
        dirpath = input('输入需要检查的文件夹路径：')
        if dirpath == '1':
            os.startfile(RULE_FILE)
            continue
        elif dirpath == '2':
            set_suffix_check(True)
            continue
        elif dirpath == '3':
            set_suffix_check(False)
            continue

        if not os.path.exists(dirpath) or os.path.isfile(dirpath):
            print('输入路径有误，请重新输入！')
            continue
        read_rules()
        filepaths = get_all_filepath(dirpath)  # 获取路径
        delete_paths = check_files_format(filepaths)  # 获取符合规则需要删除的文件路径
        show_files(delete_paths)
        if len(delete_paths) != 0:
            makesure = input('是否删除（至回收站）？(y/n)')
            if makesure.upper() == 'Y':
                delete_files(delete_paths)
                folders = get_parent_folder(delete_paths)
                delete_empty_folders(folders)


if __name__ == '__main__':
    main()
