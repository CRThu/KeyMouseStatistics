import collections

import SQLite_oper


class DataStorage(object):
    def __init__(self, sqlite_path='kmstat.db'):
        self.sqlite_path = sqlite_path
        self.sql = None

    def open(self):
        self.sql = SQLite_oper.SQLite_oper(self.sqlite_path)
        self.sql.open()
        if self.sql.is_newdb:
            self.add_mouse_moving_table()
            self.add_mouse_click_table()
            self.add_mouse_scroll_table()
            self.add_keyboard_press_table()

    def add_mouse_moving_table(self):
        self.sql.exec('CREATE TABLE MOUSE_MOVING_LOG\
                                      (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                                      TIME_START            INT           NOT NULL,\
                                      DURING                  INT                              ,\
                                      LENGTH                  DOUBLE    NOT NULL);')
        self.sql.save()

    def add_mouse_click_table(self):
        self.sql.exec('CREATE TABLE MOUSE_CLICK_LOG\
                                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                                    TIME_START            INT            NOT NULL,\
                                    DURING                  INT                              ,\
                                    KEY_UNKNOWN     INT            NOT NULL ,\
                                    KEY_LEFT                 INT            NOT NULL ,\
                                    KEY_MIDDLE           INT            NOT NULL ,\
                                    KEY_RIGHT              INT            NOT NULL );')
        self.sql.save()

    def add_mouse_scroll_table(self):
        self.sql.exec('CREATE TABLE MOUSE_SCROLL_LOG\
                                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                                    TIME_START            INT            NOT NULL,\
                                    DURING                  INT                              ,\
                                    SCROLL_UP             INT            NOT NULL ,\
                                    SCROLL_DOWN      INT            NOT NULL ,\
                                    SCROLL_LEFT          INT            NOT NULL ,\
                                    SCROLL_RIGHT       INT            NOT NULL );')
        self.sql.save()

    def add_keyboard_press_table(self):
        return self.sql.exec('CREATE TABLE KEYBOARD_PRESS_LOG\
                                      (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                                      TIME_START            INT           NOT NULL,\
                                      KEY_PRESS              TEXT                           );')

    # def is_keyboard_press_field_exist(self, field_exist_str):
    #     pos = self.sql.exec(f'select instr(sql, \'{field_exist_str}\') from sqlite_master '
    #                         f'WHERE type = \'table\' AND tbl_name = \'KEYBOARD_PRESS_LOG\';', True)
    #     # return pos[0][0]
    #     if pos[0][0] != 0:
    #         return True
    #     else:
    #         return False
    #
    # def add_keyboard_press_field(self, field_name):
    #     return self.sql.exec(f'ALTER TABLE KEYBOARD_PRESS_LOG ADD "{field_name}" int NULL;')

    def add_mouse_moving_log(self, distance, during=-1):
        if during == -1:
            during_tosql = 'NULL'
        else:
            during_tosql = str(during)

        self.sql.exec('INSERT INTO MOUSE_MOVING_LOG VALUES ('
                      + 'NULL,'  # 主键
                      + ' datetime(\'now\',\'localtime\'),'  # 时间
                      + ' %s,' % during_tosql  # 时间长度
                      + ' %f);' % distance)  # 移动距离

        self.sql.save()

    def add_mouse_click_log(self, **key):

        if 'during_time' not in key:
            during_tosql = 'NULL'
        else:
            during_tosql = str(key['during_time'])

        # print(key)

        self.sql.exec('INSERT INTO MOUSE_CLICK_LOG VALUES ('
                      + 'NULL,'  # 主键
                      + ' datetime(\'now\',\'localtime\'), '  # 时间
                      + ' %s,' % during_tosql  # 时间长度
                      + ' %d,' % key['unknown']  # KEY_UNKNOWN
                      + ' %d,' % key['left']  # KEY_LEFT
                      + ' %d,' % key['middle']  # KEY_MIDDLE
                      + ' %d);' % key['right'])  # KEY_RIGHT
        self.sql.save()

    def add_mouse_scroll_log(self, **scroll):

        if 'during_time' not in scroll:
            during_tosql = 'NULL'
        else:
            during_tosql = str(scroll['during_time'])

        # print(scroll)

        self.sql.exec('INSERT INTO MOUSE_SCROLL_LOG VALUES ('
                      + 'NULL,'  # 主键
                      + ' datetime(\'now\',\'localtime\'), '  # 时间
                      + ' %s,' % during_tosql  # 时间长度
                      + ' %d,' % scroll['up']  # SCROLL_UP
                      + ' %d,' % scroll['down']  # SCROLL_DOWN
                      + ' %d,' % scroll['left']  # SCROLL_LEFT
                      + ' %d);' % scroll['right'])  # SCROLL_RIGHT
        self.sql.save()

    def add_keyboard_press_log(self, **kp):
        self.sql.exec('INSERT INTO KEYBOARD_PRESS_LOG VALUES ('
                      + 'NULL,'  # 主键
                      + ' datetime(\'now\',\'localtime\'), '  # 时间
                      + ' \'%s\');' % kp['key_press'])  # KEY_PRESS
        self.sql.save()

    def read_mouse_moving_data(self):
        return self.sql.exec('SELECT LENGTH FROM MOUSE_MOVING_LOG;', True)

    def read_mouse_click_data(self):
        return self.sql.exec('SELECT KEY_UNKNOWN,KEY_LEFT,KEY_MIDDLE,KEY_RIGHT FROM MOUSE_CLICK_LOG;', True)

    def read_mouse_scroll_data(self):
        return self.sql.exec('SELECT SCROLL_UP,SCROLL_DOWN,SCROLL_LEFT,SCROLL_RIGHT FROM MOUSE_SCROLL_LOG;', True)

    def read_keyboard_press_data(self):
        return self.sql.exec('SELECT  KEY_PRESS FROM KEYBOARD_PRESS_LOG;', True)

    def read_keyboard_press_dict(self):
        # press_list = [x[0] for x in ds.read_keyboard_press_data()]
        # print(press_list)
        # c = collections.Counter(press_list)
        # dict(c)
        return dict(collections.Counter([x[0] for x in self.read_keyboard_press_data()]))

    def close(self):
        self.sql.close(True)


if __name__ == '__main__':
    ds = DataStorage('sql_test.db')
    ds.open()
    ds.add_mouse_moving_log(50.1234)
    ds.add_mouse_moving_log(50.4567, 30)
    print(ds.read_mouse_moving_data())

    dic = {'unknown': 20, 'left': 14, 'middle': 24, 'right': 48}
    ds.add_mouse_click_log(**dic)
    ds.add_mouse_click_log(during_time=50, **dic)
    print(ds.read_mouse_click_data())

    scl = {'up': 222, 'down': 444, 'left': 666, 'right': 777}
    ds.add_mouse_scroll_log(**scl)
    ds.add_mouse_scroll_log(during_time=50, **scl)
    print(ds.read_mouse_scroll_data())

    # print(ds.is_keyboard_press_field_exist('ID'))
    # print(ds.is_keyboard_press_field_exist('Key.ascii.65'))
    # print(ds.is_keyboard_press_field_exist('Key.ctrl_l'))
    #
    # if not ds.is_keyboard_press_field_exist('Key.ascii.65'):
    #     ds.add_keyboard_press_field('Key.ascii.65')
    # if not ds.is_keyboard_press_field_exist('Key.ctrl_l'):
    #     ds.add_keyboard_press_field('Key.ctrl_l')

    kpl = {'key_press': 'Key.ascii.97'}
    ds.add_keyboard_press_log(**kpl)
    kpl = {'key_press': 'Key.tab'}
    ds.add_keyboard_press_log(**kpl)
    # print(ds.read_keyboard_press_data())

    print(ds.read_keyboard_press_dict())

    ds.close()
