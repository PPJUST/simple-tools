"""
更新日期：
2024.03.24

功能：
pyautogui库的简单封装
"""
import random
import time
from typing import Tuple, Union

import numpy
import pyautogui
import pyperclip
from PIL import Image

# 默认参数
_DEFAULT_MOUSE_BUTTON: str = 'left'  # 默认鼠标按键
_DEFAULT_DURATION: float = 0.25  # 移动所需时间
_DEFAULT_CLICKS: int = 1  # 点击次数
_DEFAULT_INTERVAL: float = 0.1  # 间隔时间
_DEFAULT_PRESSES: int = 1  # 重复次数
_DEFAULT_CONFIDENCE = 0.9  # 寻图精度
_DEFAULT_MOVE_DIRECTION: str = '向左'  # 移动方向
_DEFAULT_MOVE_DISTANCE: int = 100  # 移动距离

_DEFAULT_SCROLL_DISTANCE: int = 100  # 滚动滚动距离

_DEFAULT_X: int = 1  # x坐标轴
_DEFAULT_Y: int = 1  # y坐标轴
_MAX_X, _MAX_Y = pyautogui.size()  # x,y坐标值的最大值限制（屏幕大小）
_DEFAULT_SCREENSHOT_IMAGE = 'screenshot.jpg'
_DEFAULT_WAIT_TIME = 1.0
_DEFAULT_WAIT_TIME_MIN = 1
_DEFAULT_WAIT_TIME_MAX = 2


def image_to_numpy_pil(image_file: str):
    """将图片转为numpy对象
     :param image_file: 图片路径
     :return: numpy.ndarray对象，图片的numpy对象"""
    image_numpy = numpy.array(Image.open(image_file))

    return image_numpy


class PyautoguiMouse:
    """pyautogui的鼠标操作的简单封装"""

    @staticmethod
    def _mouse_position() -> Tuple[int, int]:
        """获取鼠标当前位置坐标"""
        x, y = pyautogui.position()

        return x, y

    @staticmethod
    def move_mouse_to_position(x: int, y: int, duration: float = _DEFAULT_DURATION):
        """移动鼠标至指定坐标轴
        :param x: int，x坐标
        :param y: int，y坐标
        :param duration: float，移动所需时间（秒）
        """
        if x == 0 and y == 0:  # 0,0替换为1,1，防止提前终止
            x, y = 1, 1

        pyautogui.moveTo(x, y, duration=duration)

        return x, y

    @staticmethod
    def drag_mouse_to_position(x: int, y: int, button: str = _DEFAULT_MOUSE_BUTTON,
                               duration: float = _DEFAULT_DURATION):
        """按下鼠标键后拖拽至指定坐标轴
        :param x: int，x坐标
        :param y: int，y坐标
        :param button: str，鼠标按键，left/right/middle
        :param duration: float，移动所需时间（秒）
        """
        if x == 0 and y == 0:  # 0,0替换为1,1，防止提前终止
            x, y = 1, 1

        pyautogui.dragTo(x, y, button=button, duration=duration)

        return x, y

    @staticmethod
    def move_mouse_relative(move_direction: str = _DEFAULT_MOVE_DIRECTION,
                            move_distance: int = _DEFAULT_MOVE_DISTANCE, duration: float = _DEFAULT_DURATION):
        """以鼠标当前位置为基点，相对移动鼠标
        :param move_direction: str，移动方向，向左/left/向上/up/向右/right/向下/down
        :param move_distance: int，移动距离
        :param duration: float，移动所需时间（秒）
        """
        x, y = pyautogui.position()

        if move_direction in ['向左', 'left']:
            x -= move_distance
        elif move_direction in ['向右', 'right']:
            x += move_distance
        elif move_direction in ['向上', 'up']:
            y -= move_distance
        elif move_direction in ['向下', 'down']:
            y += move_distance

        if x < 0:
            x = 1
        if x > _MAX_X:
            x = _MAX_X

        if y < 0:
            y = 1
        if y > _MAX_X:
            y = _MAX_X

        if x == 0 and y == 0:
            x, y = 1, 1

        pyautogui.moveTo(x, y, duration=duration)

        return x, y

    @staticmethod
    def mouse_click(button: str = _DEFAULT_MOUSE_BUTTON, clicks: int = _DEFAULT_CLICKS,
                    interval: float = _DEFAULT_INTERVAL):
        """点击鼠标按键
        :param button: str，鼠标按键，left/right/middle
        :param clicks: int，点击次数
        :param interval: float，两次点击之间的间隔时间（秒）
        """
        pyautogui.click(button=button, clicks=clicks, interval=interval)

        return button

    @staticmethod
    def mouse_down(button: str = _DEFAULT_MOUSE_BUTTON):
        """按下鼠标按键
        :param button: str，鼠标按键，left/right/middle
        """
        pyautogui.mouseDown(button=button)

        return button

    @staticmethod
    def mouse_up(button: str = _DEFAULT_MOUSE_BUTTON):
        """释放鼠标按键
        :param button: str，鼠标按键，left/right/middle
        """
        pyautogui.mouseUp(button=button)

        return button

    @staticmethod
    def scroll_mouse_wheel(distance: int = _DEFAULT_SCROLL_DISTANCE):
        """滚动鼠标滚轮
        :param distance: int，滚动激励，正数向上滚动，负数向下滚动
        """
        pyautogui.scroll(clicks=distance)

        return distance


class PyautoguiKeyboard:
    """pyautogui的键盘操作的简单封装"""

    @staticmethod
    def press_text(message: str, presses: int = _DEFAULT_PRESSES, interval: float = _DEFAULT_INTERVAL):
        """输入字符串（通过复制粘贴实现）
        :param message: str，输入的文本
        :param presses: int，重复次数
        :param interval: float，两次输入之间的间隔时间
        """
        for _ in range(presses):
            pyperclip.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(interval)

        return message

    @staticmethod
    def press_keys(keys: Union[str, list], presses: int = _DEFAULT_PRESSES, interval: float = _DEFAULT_INTERVAL):
        """敲击指定键盘按键
        :param keys: str或list，单个或多个键盘按键，如果是多键的str需要以空格间隔（需要指定的按键名称）
        :param presses: int，重复次数
        :param interval: float，两次输入之间的间隔时间
        """
        if type(keys) is str:
            keys = keys.split(' ')

        pyautogui.press(keys=keys, presses=presses, interval=interval)

        return keys

    @staticmethod
    def press_down_key(key: str):
        """按下指定键盘按键
        :param key: str，单个键盘按键（需要指定的按键名称）"""
        pyautogui.keyDown(key)

        return key

    @staticmethod
    def press_up_key(key: str):
        """释放指定键盘按键
        :param key: str，单个键盘按键（需要指定的按键名称）"""
        pyautogui.keyUp(key)

        return key

    @staticmethod
    def press_hotkey(hotkeys: Union[list, str]):
        """按下组合键盘按键，用于实现热键操作
        :param hotkeys: str或list，单个或多个键盘按键，如果是多键的str需要以空格间隔（需要指定的按键名称）"""
        if type(hotkeys) is str:
            hotkeys = hotkeys.split(' ')

        pyautogui.hotkey(hotkeys)

        return hotkeys


class PyautoguiImage:
    """pyautogui的图像操作的简单封装

    pyautogui库关于图像的操作调用了PyScreeze库
    如果指定了confidence参数，则需要安装opencv库"""

    @staticmethod
    def screenshot_fullscreen(pic: str = _DEFAULT_SCREENSHOT_IMAGE):
        """全屏截图并保存到本地图片
        :param pic: str，保存的图片
        """
        pyautogui.screenshot(pic)

        return pic

    @staticmethod
    def screenshot_area(area: Union[tuple, list], pic: str = 'screenshot.png'):
        """指定区域截图并保存到本地图片
        :param area: tuple或list，截图区域，参数为(左上角X坐标值, 左上角Y坐标值, 右下角X坐标值, 右下角X坐标值)
        :param pic: str，保存的图片
        """
        region = (area[0], area[1], area[2] + area[0], area[3] + area[1])  # 转换area参数至pyautogui的格式
        pyautogui.screenshot(pic, region=region)

        return pic

    @staticmethod
    def _search_first_position(pic: str,
                               confidence: float = _DEFAULT_CONFIDENCE
                               ) -> Union[tuple, None]:
        """在屏幕上搜索图片，获取其第一次匹配到的中心点坐标
        :param pic: str，需要搜索的图片
        :param confidence: float，搜索精度，0~1
        :return: 元组(x, y)或None
        """
        numpy_pic = image_to_numpy_pil(pic)
        position = pyautogui.locateCenterOnScreen(numpy_pic, confidence=confidence)

        if position:
            loc = (position.x, position.y)
            return loc
        else:
            return None

    @staticmethod
    def _search_all_position(pic: str, confidence: float = _DEFAULT_CONFIDENCE, timeout: int = 60) -> list:
        """在屏幕上搜索图片，获取其全部匹配到的中心点坐标
        :param pic: str，需要搜索的图片
        :param confidence: float，搜索精度，0~1
        :param timeout: int，超时时间（秒）
        :return: list，[(x1, y1), (x2, y2)...]
        """
        numpy_pic = image_to_numpy_pil(pic)
        time_start = time.time()
        positions = []
        while True:
            result = pyautogui.locateAllOnScreen(numpy_pic, confidence=confidence)
            for pos in result:
                mid_x = pos.left + pos.width // 2
                mid_y = pos.top + pos.height // 2
                positions.append((mid_x, mid_y))
            if positions:
                break

            time_current = time.time()
            run_time = time_start - time_current
            if run_time >= timeout:
                break
            else:
                time.sleep(_DEFAULT_INTERVAL)

        return positions

    @staticmethod
    def move_to_pic(pic, duration=_DEFAULT_DURATION, search_mode: str = '第一个',
                    confidence: float = _DEFAULT_CONFIDENCE,
                    timeout: int = 60) -> bool:
        """在屏幕上搜索图片，并移动到该图片上
        :param pic: str，需要搜索的图片
        :param duration: float，移动所需时间（秒）
        :param search_mode: str，查找模式，第一个/first/全部/all
        :param confidence: float，搜索精度，0~1
        :param timeout: int，超时时间（秒）
        """
        positions = PyautoguiImage._search_all_position(pic, confidence=confidence, timeout=timeout)
        if positions:
            if search_mode in ['第一个', 'first']:
                x, y = positions[0]
                PyautoguiMouse.move_mouse_to_position(x=x, y=y, duration=duration)
            elif search_mode in ['全部', 'all']:
                for x, y in positions:
                    PyautoguiMouse.move_mouse_to_position(x=x, y=y, duration=duration)
            return True
        else:
            return False

    @staticmethod
    def click_pic(pic, duration=_DEFAULT_DURATION,
                  button: str = _DEFAULT_MOUSE_BUTTON, clicks: int = _DEFAULT_CLICKS,
                  interval: float = _DEFAULT_INTERVAL, search_mode: str = '第一个',
                  confidence: float = _DEFAULT_CONFIDENCE,
                  timeout: int = 60) -> bool:
        """在屏幕上搜索图片，并点击该图片
        :param pic: str，需要搜索的图片
        :param duration: float，移动所需时间（秒）
        :param button: str，鼠标按键，left/right/middle
        :param clicks: int，点击次数
        :param interval: float，两次点击之间的间隔时间（秒）
        :param search_mode: str，查找模式，第一个/first/全部/all
        :param confidence: float，搜索精度，0~1
        :param timeout: int，超时时间（秒）
        """
        positions = PyautoguiImage._search_all_position(pic, confidence=confidence, timeout=timeout)
        if positions:
            if search_mode in ['第一个', 'first']:
                x, y = positions[0]
                PyautoguiMouse.move_mouse_to_position(x=x, y=y, duration=duration)
                PyautoguiMouse.mouse_click(button=button, clicks=clicks, interval=interval)
            elif search_mode in ['全部', 'all']:
                for x, y in positions:
                    PyautoguiMouse.move_mouse_to_position(x=x, y=y, duration=duration)
                    PyautoguiMouse.mouse_click(button=button, clicks=clicks, interval=interval)
            return True
        else:
            return False


class PyautoguiCustom:
    """pyautogui的其他操作的简单封装"""

    @staticmethod
    def wait_time(wait_time: float = _DEFAULT_WAIT_TIME):
        """等待指定时间
        :param wait_time: float，等待时间"""
        if wait_time == 0:
            wait_time = 0.01

        time.sleep(wait_time)

        return wait_time

    @staticmethod
    def wait_time_random(wait_time_min: int = _DEFAULT_WAIT_TIME_MIN, wait_time_max: int = _DEFAULT_WAIT_TIME_MAX):
        """等待随机时间
        :param wait_time_min: int，随机时间的下限
        :param wait_time_max: int，随机时间的上限"""
        wait_time_random = round(random.uniform(wait_time_min, wait_time_max), 2)

        if wait_time_random == 0:
            wait_time_random = 0.01

        time.sleep(wait_time_random)

        return wait_time_random
