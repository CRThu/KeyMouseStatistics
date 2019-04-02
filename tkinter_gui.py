import time
import tkinter as tk
import threading
import DataStorage as ds


class AppUI(object):
    def __init__(self):
        # 窗口框架
        self.form = tk.Tk()
        self.form.title("Key&Mouse Statistics")
        self.form.geometry("700x500")
        self.create_ui()
        self.form.mainloop()

    def hit_me(self):
        sql = ds.DataStorage()
        sql.open()

        # 读取鼠标移动数据
        self.loading['text'] = 'loading mouse moving data...'
        self.loading.update()
        mouse_moving_sum = 0
        for i in sql.read_mouse_moving_data():
            mouse_moving_sum += i[0]
        self.loading['text'] = ''
        self.loading.update()
        self.mms['text'] = 'mouse moving distance : ' + '%.2f cm.' % (mouse_moving_sum / 86.825)
        self.mms.update()

        self.loading['text'] = 'loading mouse click data...'
        self.loading.update()
        mouse_click_sum = [0, 0, 0, 0]
        for i in sql.read_mouse_click_data():
            for c in range(4):
                mouse_click_sum[c - 1] += i[c - 1]
        self.loading['text'] = ''
        self.loading.update()
        self.mct['text'] = 'mouse click times : U:%d, L:%d, M:%d, R:%d.' \
                           % (mouse_click_sum[0], mouse_click_sum[1], mouse_click_sum[2], mouse_click_sum[3])
        self.mct.update()

        self.loading['text'] = 'loading mouse scroll data...'
        self.loading.update()
        mouse_scroll_sum = [0, 0, 0, 0]
        for i in sql.read_mouse_scroll_data():
            for c in range(4):
                mouse_scroll_sum[c - 1] += i[c - 1]
        self.loading['text'] = ''
        self.loading.update()
        self.mst['text'] = 'mouse scroll times : ↑:%d, ↓:%d, ←:%d, →:%d.' \
                           % (mouse_scroll_sum[0], mouse_scroll_sum[1], mouse_scroll_sum[2], mouse_scroll_sum[3])
        self.mst.update()

        self.loading['text'] = 'loading mouse scroll data...'
        self.loading.update()

        self.kpt['text'] = 'keyboard press times : %d.' % sum(sql.read_keyboard_press_dict().values())
        self.kpt.update()

        self.loading['text'] = ''
        self.loading.update()

        sql.close()

    def create_ui(self):
        # Label
        self.mms = tk.Label(self.form,
                            text='mouse moving distance : NaN cm.',
                            font=('Arial', 12),
                            width=45, height=2)
        self.mms.pack()

        self.mct = tk.Label(self.form,
                            text='mouse click times : U:NaN, L:NaN, M:NaN, R:NaN.',
                            font=('Arial', 12),
                            width=45, height=2)
        self.mct.pack()

        self.mst = tk.Label(self.form,
                            text='mouse scroll times : ↑:NaN, ↓:NaN, ←:NaN, →:NaN.',
                            font=('Arial', 12),
                            width=45, height=2)
        self.mst.pack()

        self.kpt = tk.Label(self.form,
                            text='keyboards press times : NaN.',
                            font=('Arial', 12),
                            width=45, height=2)
        self.kpt.pack()

        # Button
        self.refreshButton = tk.Button(self.form,
                                       text='刷新',  # 显示按钮文字
                                       width=15, height=2,
                                       command=self.hit_me)  # 点击按钮执行命令
        self.refreshButton.pack()  # 放置按钮

        # loading database
        self.loading = tk.Label(self.form,
                                text=' ',
                                font=('Arial', 12),
                                width=45, height=2)
        self.loading.pack()


if __name__ == '__main__':
    # 启动记录线程
    t = threading.Thread(target=AppUI, name='AppUI')
    t.start()
    # t.join()  # 可能需要注释
    # print('hw')
