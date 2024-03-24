"""
更新日期：
2024.03.24

功能：
修复pynput模块中HotKey类的问题，使其能够正确识别小键盘数字
"""
from pynput import keyboard


class HotKeyFix(keyboard.HotKey):
    def __init__(self, keys, on_activate):
        super().__init__(keys, on_activate)

    def press(self, key):
        setattr(key, '_scan', None)
        super().press(key)

    def release(self, key):
        setattr(key, '_scan', None)
        super().release(key)


class GlobalHotKeysFix(keyboard.Listener):
    def __init__(self, hotkeys, *args, **kwargs):
        self._hotkeys = [
            HotKeyFix(HotKeyFix.parse(key), value)
            for key, value in hotkeys.items()]
        super(GlobalHotKeysFix, self).__init__(
            on_press=self._on_press,
            on_release=self._on_release,
            *args,
            **kwargs)

    def _on_press(self, key):
        for hotkey in self._hotkeys:
            hotkey.press(self.canonical(key))

    def _on_release(self, key):
        for hotkey in self._hotkeys:
            hotkey.release(self.canonical(key))


"""下面方法可行，但不优美
class HotKeyFix(keyboard.HotKey):
    def __init__(self, keys, on_activate):
        super().__init__(keys, on_activate)

    def press(self, key):
        keys_str = [str(i) for i in self._keys]
        if str(key) in keys_str and key not in self._state:
            self._state.add(key)
            if [str(i) for i in self._state] == [str(i) for i in self._keys]:
                self._on_activate()
"""
