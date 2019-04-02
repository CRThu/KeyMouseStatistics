import sys
import time
import threading
import win32api, win32con, win32gui  # win32ui打包时包含MFC DLL

import GetAdmin
import MouseHookListenerClass as mhl
import KeyboardHookListenerClass as khl
import DataStorage as ds
import tkinter_gui as tkgui
import stdout_to_log as log

# 避免重复打开
hwnd = win32gui.FindWindow(0, 'Key&Mouse Statistics')
if hwnd != 0:
    win32gui.SetForegroundWindow(hwnd)
    sys.exit()

sys.stdout = log.Logger()

print("-------------   Log start   -------------")
print(time.strftime("--------   %Y-%m-%d %H:%M:%S   --------", time.localtime()))
print('stdout >> log.')

getAdmin = GetAdmin.GetAdmin(__file__)
getAdmin.get_admin()

if getAdmin.is_admin():

    # 启动鼠标监听
    mhl = mhl.MouseHookListenerClass()
    mhl.start()

    # 启动数据库记录
    ds1 = ds.DataStorage()
    ds1.open()

    during_time = 5
    is_gui_exit = False


    def MKStorageThreadLoop():
        global is_gui_exit
        while not is_gui_exit:
            # 启动鼠标移动距离记录线程
            time.sleep(during_time)
            print(mhl.distance_sum)
            ds1.add_mouse_moving_log(mhl.distance_sum, during_time)
            mhl.clear_mouse_moving_distance_sum()

            # 启动鼠标按键记录线程
            print(mhl.mouse_button_click_sum)
            ds1.add_mouse_click_log(during_time=during_time, **mhl.mouse_button_click_sum)
            mhl.clear_mouse_button_click_sum()

            # 启动鼠标滚动记录线程
            print(mhl.mouse_scroll_sum)
            ds1.add_mouse_scroll_log(during_time=during_time, **mhl.mouse_scroll_sum)
            mhl.clear_mouse_scroll_sum()


    mkst = threading.Thread(target=MKStorageThreadLoop, name='MKStorageThread')
    mkst.start()


    def KeyStorageFunc(k_str):
        ds1.add_keyboard_press_log(key_press=k_str)
        print(k_str)


    # 启动键盘按键记录线程
    khl = khl.KeyboardHookListenerClass(KeyStorageFunc)
    khl.start()

    # 启动GUI
    uit = threading.Thread(target=tkgui.AppUI, name='AppUI')
    uit.start()
    uit.join()  # 阻塞线程

    # 关闭其余线程
    is_gui_exit = True
    mhl.stop()
    khl.stop()
    while mkst.is_alive():
        time.sleep(1)
        print('wait for mkst exit...')

    print("-------------   Log  stop   -------------")
    print(time.strftime("--------   %Y-%m-%d %H:%M:%S   --------", time.localtime()))

else:
    print('permission denied!')
    win32api.MessageBox(0, "没有取得管理员权限", "Error!", win32con.MB_OK)
