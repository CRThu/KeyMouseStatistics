import os
import sqlite3
import random
import time

is_lock = False


class SQLite_oper(object):
    def __init__(self, sqlite_path):
        self.sqlite_path = sqlite_path
        self.is_newdb = None
        self.conn = None
        self.cursor = None
        self.is_open = None

    def open(self):
        self.is_newdb = not os.path.exists(self.sqlite_path)
        # 遇到此错误:SQLite objects created in a thread can only be used in that same thread
        # 设置:check_same_thread=False
        self.conn = sqlite3.connect(self.sqlite_path, check_same_thread=False)  # 建立连接,若不存在将创建
        self.cursor = self.conn.cursor()  # 创建cursor
        # print("Open database successfully")
        self.is_open = True

    def exec(self, cmd, output_return=False):
        global is_lock
        while is_lock:
            # print("exec() busy!")
            time.sleep(0.005)
        is_lock = True
        self.cursor.execute(cmd)
        is_lock = False
        if output_return:
            return self.cursor.fetchall()

    def save(self):
        self.conn.commit()  # 提交事务

    def close(self, save):
        if save:
            self.save()
        self.cursor.close()  # 关闭cursor
        self.conn.close()  # 关闭连接
        self.is_open = False


if __name__ == '__main__':
    sql = SQLite_oper('sql_test.db')
    sql.open()
    if sql.is_newdb:
        sql.exec('CREATE TABLE MOUSE_MOVING_LOG\
                  (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                  TIME_START            INT           NOT NULL,\
                  DURING                  INT                              ,\
                  LENGTH                  DOUBLE    NOT NULL);')

    for i in range(10):
        sql.exec(f'INSERT INTO MOUSE_MOVING_LOG VALUES (NULL,datetime(\'now\',\'localtime\') ,NULL,{random.random()});')
        print(i)
        time.sleep(0.5)
    sql.close(True)
