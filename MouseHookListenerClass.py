import math

from pynput import mouse  # 控制与监听鼠标或触摸板类


class MouseHookListenerClass(object):

    def __init__(self):
        self.pos_x = None
        self.pos_y = None
        self.distance_sum = 0
        self.mouse_button_click_sum = {'unknown': 0, 'left': 0, 'middle': 0, 'right': 0}
        self.mouse_scroll_sum = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        self.listener = None

    def clear_mouse_moving_distance_sum(self):
        self.distance_sum = 0

    def clear_mouse_button_click_sum(self):
        self.mouse_button_click_sum = {'unknown': 0, 'left': 0, 'middle': 0, 'right': 0}

    def clear_mouse_scroll_sum(self):
        self.mouse_scroll_sum = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

    def mouse_on_move(self, x, y):
        if self.pos_x is not None:
            distance = math.sqrt(abs(self.pos_x - x) ** 2 + abs(self.pos_y - y) ** 2)
            # 2880*1800下对角线长度为3396.23px
            self.distance_sum += distance
            # print(self.distance_sum)
            # print(f"mouse moving to {(x,y)}")
        self.pos_x = x
        self.pos_y = y

    def mouse_on_click(self, x, y, button, pressed):
        # 按下按键时记录
        if pressed:
            if button == mouse.Button.unknown:
                self.mouse_button_click_sum['unknown'] += 1
            if button == mouse.Button.left:
                self.mouse_button_click_sum['left'] += 1
            if button == mouse.Button.middle:
                self.mouse_button_click_sum['middle'] += 1
            if button == mouse.Button.right:
                self.mouse_button_click_sum['right'] += 1
        # pass
        # print(f"{button} pressed:{pressed}, at {(x,y)}")
        # if not pressed:
        #   # 停止监听
        #   return False

    def mouse_on_scoll(self, x, y, dx, dy):
        if dx > 0:
            self.mouse_scroll_sum['right'] += 1
        if dx < 0:
            self.mouse_scroll_sum['left'] += 1
        if dy > 0:
            self.mouse_scroll_sum['up'] += 1
        if dy < 0:
            self.mouse_scroll_sum['down'] += 1
        # print(f"mouse scroll {dx,dy}")
        # print(self.mouse_scroll_sum)
        # pass

    def join(self):
        # 线程监听事件,直到鼠标释放
        # 停止监听方法:返回False或调用pynput.mouse.Listener.stop发起StopException异常
        with mouse.Listener(
                on_move=self.mouse_on_move,
                on_click=self.mouse_on_click,
                on_scroll=self.mouse_on_scoll) as self.listener:
            self.listener.join()

    def start(self):
        # a non-blocking fashion
        self.listener = mouse.Listener(
            on_move=self.mouse_on_move,
            on_click=self.mouse_on_click,
            on_scroll=self.mouse_on_scoll)
        self.listener.start()

    def stop(self):
        self.listener.stop()


if __name__ == '__main__':
    mhl = MouseHookListenerClass()
    mhl.join()
