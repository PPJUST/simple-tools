"""
更新日期：
-.-.-

功能：
删除某个文件夹下已经失效的快捷方式
"""


import configparser
import os

import send2trash
import win32com.client

time_autorun = 0


def get_original_path(shortcut_path):
    """获取一个快捷方式指向的路径"""
    try:
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        return shortcut.Targetpath
    except Exception as e:
        return f"Error: {e}"


def set_check_folder(back_to_main: bool = True):
    """设置需要检查的文件夹路径
    back_to_main 参数决定是否返回main函数"""
    while True:
        input_folder = input('输入需要检查的文件夹路径：').strip()
        if input_folder and os.path.exists(input_folder) and os.path.isdir(input_folder):
            break
        else:
            print('输入路径有误，请重新输入。')

    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('DEFAULT', 'check_folder', input_folder)
    config.write(open('config.ini', 'w'))

    if back_to_main:
        main()
    else:
        return input_folder


def set_autorun():
    """设置自动执行选项"""
    while True:
        input_code = int(input('设置是否自动执行（1为是，2为否）：'))
        if input_code in [1, 2]:
            break
        else:
            '输入格式有误，请重新输入。'

    if input_code == 1:
        a_c = True
    else:
        a_c = False

    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('DEFAULT', 'autorun', str(a_c))
    config.write(open('config.ini', 'w'))

    main()


def get_config_setting(key: str) -> str:
    """获取配置文件中指定key的value"""
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config.get('DEFAULT', key)


def create_config():
    """检查配置文件是否存在，如不存在则新建"""
    if not os.path.exists('config.ini'):
        with open('config.ini', 'w') as cw:
            the_settings = """[DEFAULT]
autorun = False
check_folder = 
    """
            cw.write(the_settings)


def start():
    check_folder = get_config_setting('check_folder')
    if not check_folder or not os.path.exists(check_folder):
        print('指定路径不存在')
        new_check_folder = set_check_folder(back_to_main=False)
    else:
        new_check_folder = check_folder

    for filename in os.listdir(new_check_folder):
        fullpath = os.path.join(new_check_folder, filename)
        if os.path.isfile(fullpath) and fullpath.lower().endswith('.lnk') and os.path.getsize(fullpath) < 1048576:
            original_path = get_original_path(fullpath)
            print(f'---{filename} 的原文件路径为 {original_path}')
            if not os.path.exists(original_path):
                send2trash.send2trash(fullpath)
                print(f'======已删除 {filename}')
    print('已检查所有快捷方式')

    global time_autorun
    time_autorun += 1
    main()


def main():
    """初始执行"""
    create_config()

    check_folder = get_config_setting('check_folder')
    autorun = get_config_setting('autorun')

    info = f'''
    ================================================
    本工具用于检查指定文件夹下的所有lnk快捷方式对应的目标路径是否存在，
    如果目标路径不存在，则删除该lnk快捷方式文件至回收站
    ------------------------
    当前【检查的文件夹路径】设置：{check_folder}
    当前【自动执行】设置：{autorun}
    ================================================'''
    print(info)

    code_info = """
    输入指定数字进行相应操作:
    1. 执行检查
    2. 退出
    3. 设置【检查的文件夹路径】
    4. 设置【自动执行】
    """

    if autorun == 'True' and os.path.exists(check_folder) and time_autorun == 0:
        input_code = 1
    else:
        while True:
            input_code = int(input(code_info))
            if input_code in [1, 2, 3, 4]:
                break
            else:
                '无对应输入代码，请重试'

    if input_code == 1:
        start()
    elif input_code == 2:
        quit()
    elif input_code == 3:
        set_check_folder()
    elif input_code == 4:
        set_autorun()


if __name__ == "__main__":
    main()
