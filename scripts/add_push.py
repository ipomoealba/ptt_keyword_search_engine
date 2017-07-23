#!/bin/python
# -*- encoding: utf-8 -*-
import multiprocessing
import MySQLdb
import sys
import traceback
import json
from multiprocessing import Process
from db_helper import DBConn


class change_push(Process):

    def __init__(self, query):
        self.query = query

    def run():
        pass

try:
    for i in range(0, 10000):
        dbuse = DBConn()
        dbuse.dbConnect()
        sql = "SELECT * FROM Reply ORDER BY `pid` limit %d,10" % (10 * i)
        dbuse.runQuery(sql)
        result = dbuse.results
        dbuse.dbClose()
        for i in result:
            push = 0
            sheee = 0
            arrow = 0
            reply_raw = i[1]
            reply = []
            if reply_raw != u'[]':
                tmp = reply_raw[2:-2].split('}, {')
                for i, w in enumerate(tmp):
                    try:
                        reply.append([
                            w[w.index(""", "push_tag": """ ) + len(""", "push_tag": \"""")
                              :w.index("""", "push_date":""")],
                            w[w.index(""", "push_user": """) +
                              len(""", "push_user": \""""):w.index("""", "push_tag""")],
                            w[w.index("""push_content": ":""") +
                              len("""push_content": ":"""):w.index('", "push_user": ')],
                            w[w.index(""", "push_date": """) + len(""", "push_date": \""""):w.index("\n")]])

                    except Exception:
                        print("failed")

            for r in reply:
                if r:
                    if u'推' in r[0][0]:
                        push += 1
                    elif u'噓' in r[0][0]:
                        sheee += 1
                    else:
                        arrow += 1

            try:
                print(push)
                print(sheee)
                print(arrow)
                dbuse2 = DBConn()
                dbuse2.dbConnect()
                sql = "UPDATE Gossiping SET `push` = %d, `sheee` = %d, `arrow` = %d Where `pid` = %s" % (
                    push, sheee, arrow, result[0])
                dbuse2.runUpdate(sql)
                dbuse2.dbClose()
            except Exception:
                pass

except:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    print "MySQL DB Error"
