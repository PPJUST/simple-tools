"""
更新日期：
-.-.-

功能：
抓取Github的Hosts，并写入本地hosts文件，加速国内访问Github的速度
"""

import shutil
import subprocess
import time
from typing import Union

import requests

_HOSTS_FILE = r'C:\Windows\System32\drivers\etc\hosts'
_HOSTS_URL_FetchGitHub = 'https://hosts.gitcdn.top/hosts.txt'
_HOSTS_URL_Github520 = 'https://raw.hellogithub.com/hosts'


def get_url_hosts_list(url) -> Union[list, bool]:
    """读取网络hosts"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    hosts_html = response.text

    if hosts_html:
        print('已获取hosts列表')
    else:
        return False

    hosts_html_list = hosts_html.splitlines()
    hosts_html_list = [i + '\n' for i in hosts_html_list]

    return hosts_html_list


def get_local_hosts_list() -> list:
    """读取本地hosts"""
    with open(_HOSTS_FILE, 'r', encoding='utf-8') as f:
        hosts_local = f.readlines()

    return hosts_local


def clear_hosts_github():
    """删除本地hosts中的github相关host"""
    local_hosts = get_local_hosts_list()
    new_hosts = local_hosts
    # 删除FetchGitHub
    if '# fetch-github-hosts begin\n' in new_hosts:
        begin = new_hosts.index('# fetch-github-hosts begin\n')
        end = new_hosts.index('# fetch-github-hosts end\n')
        new_hosts = new_hosts[:begin] + new_hosts[end + 1:]

    if '# GitHub520 Host Start\n' in new_hosts:
        begin = new_hosts.index('# GitHub520 Host Start\n')
        end = new_hosts.index('# GitHub520 Host End\n')
        new_hosts = new_hosts[:begin] + new_hosts[end + 1:]

    with open(_HOSTS_FILE, 'w', encoding='utf-8') as hw:
        hw.writelines(new_hosts)
    flush_dns()


def flush_dns():
    """刷新DNS缓存"""
    subprocess.run(['ipconfig', '/flushdns'], shell=True)


def add_local_hosts(hosts_list: list):
    """添加host到本地hosts"""
    if hosts_list:
        backup_hosts()
        clear_hosts_github()
        local_hosts = get_local_hosts_list()

        join_hosts = local_hosts + hosts_list

        with open(_HOSTS_FILE, 'w', encoding='utf-8') as hw:
            hw.writelines(join_hosts)  # 注意 列表中的每一个元素后都需要有\n换行符

        flush_dns()
        print('已更新hosts')
    else:
        print('hosts更新失败')


def backup_hosts():
    """备份hosts"""
    shutil.copyfile(_HOSTS_FILE, f'hosts_{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}')


def main():
    info = '0.恢复hosts\n1.更新hosts-Github520\n2.更新hosts-FetchGitHub\n9.退出\n'
    print(info)
    while True:
        code = input('输入对应代码：')
        if code == '0':  # 清除github相关host
            clear_hosts_github()
            print('已恢复hosts')
        elif code == '1':  # Github520
            hosts_url = get_url_hosts_list(_HOSTS_URL_Github520)
            add_local_hosts(hosts_url)
        elif code == '2':  # FetchGitHub
            hosts_url = get_url_hosts_list(_HOSTS_URL_FetchGitHub)
            add_local_hosts(hosts_url)
        elif code == '9':
            quit()


if __name__ == '__main__':
    main()
