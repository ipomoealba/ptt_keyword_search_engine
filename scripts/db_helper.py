#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb


class DBConn:

    def __init__(self):
        self.user = 'root'
        self.host = 'localhost'
        self.passwd = 'admin'
        self.dbname = 'ptt'

    def dbConnect(self):
        self.db = MySQLdb.connect(
            self.host, self.user, self.passwd, self.dbname, charset='utf8')
        self.cursor = self.db.cursor()
        self.db.autocommit(True)

    # Exec SQL Query
    def runQuery(self, sql):
        self.cursor.execute(sql)
        self.results = self.cursor.fetchall()

    # Exec SQL Insert
    def runInsert(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    # Exec SQL Update
    def runUpdate(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    # Exec SQL Delete
    def runDelete(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    # 關閉資料庫連線
    def dbClose(self):
        self.db.close()
