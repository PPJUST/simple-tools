import ctypes
import pickle
import socket
import sys
import tkinter.messagebox

_HOST = '127.0.0.1'
_PORT = 9527


def is_app_running():
    """使用互斥体检查是否已经打开了一个实例"""
    mutex_name = 'MyProgram'
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        ctypes.windll.kernel32.CloseHandle(mutex)
        return True
    return False


def check_software_is_running(data):
    """向指定本地端口发送数据"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (_HOST, _PORT)
    sock.connect(server_address)

    try:
        # 发送数据
        serialized_data = pickle.dumps(data)  # 用pickle序列化，能方便地发送更多类型的数据
        sock.sendall(serialized_data)
    finally:
        # 关闭连接
        sock.close()


def listen_socket():
    """监听端口"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((_HOST, _PORT))
    sock.listen(2)
    while True:
        connection, client_address = sock.accept()
        try:
            # 接收数据
            data = connection.recv(1024)
            if data:
                non_serialized_data = pickle.loads(data)
        finally:
            # 关闭连接
            connection.close()


if __name__ == "__main__":
    if is_app_running():
        # 弹出提示
        tkinter.Tk().withdraw()
        tkinter.messagebox.showwarning(title='错误', message='程序已经运行！')
        sys.exit(1)
        # 发送数据
        # send_data_to_host('test')
    else:
        # 程序主逻辑
        pass
