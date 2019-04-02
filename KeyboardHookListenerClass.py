from pynput import keyboard  # 控制与监听鼠标或触摸板类


class KeyboardHookListenerClass(object):
    def __init__(self, key_storage_func):
        self.key_storage_func = key_storage_func
        self.listener = None
        # pass

    def keyboard_on_press(self, key):
        k = str(key)
        if (len(k) == 3 and k[0] == '\'' and k[2] == '\'') or k == '"\'"' or k == '\'\\\\\'':  # ascii
            k_str = 'Key.ascii.' + str(ord(k[1]))
        else:  # non-ascii
            k_str = str(k)

        self.key_storage_func(k_str)

        # try:
        #     print(f"{key.Char} press")
        # except AttributeError:
        #     print(f"{key} press")

    def keyboard_on_release(self, key):
        pass
        # print(f"{key} release")
        # if key == keyboard.Key.esc:
        # 停止监听
        #    return False

    def join(self):
        # 线程监听事件,直到按键释放
        # 停止监听方法:返回False或调用pynput.keyboard.Listener.stop发起StopException异常
        with keyboard.Listener(
                on_press=self.keyboard_on_press,
                on_release=self.keyboard_on_release)as self.listener:
            self.listener.join()

    def start(self):
        # a non-blocking fashion
        self.listener = keyboard.Listener(
            on_press=self.keyboard_on_press,
            on_release=self.keyboard_on_release)
        self.listener.start()

    def stop(self):
        self.listener.stop()


if __name__ == '__main__':
    def key_storage_func(k_str):
        print(k_str)


    khl = KeyboardHookListenerClass(key_storage_func)
    khl.join()
