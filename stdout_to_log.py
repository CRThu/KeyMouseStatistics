import os
import sys


class Logger(object):
    def __init__(self, filename="debug_out.log"):
        self.filename = filename
        self.terminal = sys.stdout
        # self.log = None
        self.log = open(self.filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()  # 需要此函数, 刷新数据至文件
        # self.log.close()

    def flush(self):
        pass


if __name__ == '__main__':
    sys.stdout = Logger('test_out.log')

    print('test print() >> file.')
    print('helloworld')
    print(os.path.abspath(os.path.dirname(__file__)))
    print(sys.getfilesystemencoding())
