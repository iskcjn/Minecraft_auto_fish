import cv2
import numpy as np
import keyboard
import pyautogui
import win32api, win32con, win32gui
import 获取句柄 as JUBIN
from time import sleep
from PIL import Image, ImageGrab

Handle = 0

def get_window_pos(name):
    handle = Handle

    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        # 返回坐标值和handle
        return win32gui.GetWindowRect(handle), handle


def Grab(x1, y1, x2, y2):
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(Hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # 设为高亮
    win32gui.SetForegroundWindow(Hwnd)
    # 截图
    grab_image = ImageGrab.grab((x1, y1, x2, y2))
    img = cv2.cvtColor(np.asarray(grab_image), cv2.COLOR_RGB2BGR)
    return img


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print('Start')
    pyautogui.PAUSE = 1
    sleep(3)
    STOP = True
    NUM = 0
    # 最大 最小
    MAX = 2600
    MIN = 100

    Name = "Minecraft Forge"
    JUBIN.GetHwnd(Name)
    with open("Hwnd.txt", "r") as file:
        Handle = int(file.read())
    file.close()
    print(Handle)

    while True:
        # 检测是否按下了esc键 开启
        if keyboard.is_pressed('r') and STOP:
            # break  # 退出循环
            STOP = False
            print("开始钓鱼")
        elif keyboard.is_pressed('U') and not STOP:
            STOP = True
            print("暂停钓鱼")
        if keyboard.is_pressed('y'):
            print("结束")
            break
        if not STOP:
            try:
                (x1s, y1s, x2s, y2s), Hwnd = get_window_pos(Name)
                imps = Grab(x1s, y1s, x2s, y2s)
                if imps is None:
                    print("图像空")
                else:
                    imgs = cv2.resize(imps, None, None, 2, 2)
                    size = imgs.shape
                    y0 = int(200)
                    y1 = int(size[0] / 2)
                    x0 = int(size[1] / 2 - 200)
                    x1 = int(size[1] / 2 + 250)
                    img = imgs[y0:y1, x0:x1]
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    cv2.imshow("hsv", hsv)
                    erode_hsv = cv2.erode(hsv, None, iterations=2)
                    ball_color = 'red'
                    color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
                                  'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
                                  'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
                                  }
                    inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'],
                                              color_dist[ball_color]['Upper'])
                    cv2.imshow("color", inRange_hsv)
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40))
                    dilated = cv2.dilate(inRange_hsv, kernel)  # 膨胀
                    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                    if len(contours) == 1:
                        if MIN < cv2.contourArea(contours[0]) < MAX:
                            # 外接图形
                            x, y, w, h = cv2.boundingRect(contours[0])
                            tmp3 = img.copy()
                            res4 = cv2.rectangle(tmp3, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            cv2.imshow('rectangle', res4)
                    elif len(contours) != 1:
                        cv2.waitKey(500)
                        if len(contours) != 1:
                            # cv2.imshow("img",img)
                            x, y = pyautogui.position()
                            pyautogui.click(x, y, button='right')  # 单击右键
                            NUM += 1
                            print("钓到" + str(NUM) + "条")
                    cv2.waitKey(100)
            except Exception as e:
                print(e)
    print("End")
