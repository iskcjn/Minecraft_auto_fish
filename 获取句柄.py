import ctypes
from ctypes import wintypes

WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def GetHwnd(name):
    def enum_windows_proc(hwnd, lParam):
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        title = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, title, length + 1)
        if name in title.value:
            class_name = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(hwnd, class_name, 256)
            # print("窗口句柄:", hwnd)
            with open("Hwnd.txt", "w") as file:
                file.write(str(hwnd))
            file.close()
            print("窗口标题:", title.value)
            print("窗口类名:", class_name.value)
            return False
        return True
    ctypes.windll.user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)