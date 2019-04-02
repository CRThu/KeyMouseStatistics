import ctypes, sys


class GetAdmin(object):
    def __init__(self, main):
        self.main = main

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def get_admin(self):
        if self.is_admin():
            pass
            # 将要运行的代码加到这里
        else:
            # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, self.main, None, 1)


if __name__ == '__main__':
    getAdmin = GetAdmin(__file__)
    getAdmin.get_admin()
    if getAdmin.is_admin():
        print('helloworld!')
    else:
        print('permission denied!')
        exit(0)
