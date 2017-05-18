#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import sys
import traceback
import threadpool
from db_helper import DBConn


try:
    dbuse = DBConn()
    dbuse.dbConnect()
    sql = "SELECT `pid`,`title` FROM Gossiping where first_page = False"
    dbuse.runQuery(sql)
    result = dbuse.results
    dbuse.dbClose()
    for i in result:
        if i[1].startswith("Re: "):
            db_checker = DBConn()
            db_checker.dbConnect()
            sql_checker = "SELECT count(*) FROM Gossiping WHERE title = \'%s\'" % (
                i[1][4:])
            db_checker.runQuery(sql_checker)
            checker = db_checker.results
            db_checker.dbClose()

            db_changer = DBConn()
            db_changer.dbConnect()
            if checker[0][0] != 0L:
                sql_changer = "UPDATE Gossiping SET first_page = 0 WHERE pid = \'%s\'" % (i[
                                                                                               0])

            else:
                sql_changer = "UPDATE Gossiping SET first_page = 1 WHERE pid = \'%s\'" % (i[
                                                                                               0])
            db_changer.runUpdate(sql_changer)
            db_changer.dbClose()
            print sql_checker
        else:
            try:
                db_counter = DBConn()
                db_counter.dbConnect()
                sql_get_re_num = "SELECT count(*) FROM Gossiping WHERE title = \'%s\'" % (
                    "Re: " + i[1])
                db_counter.runQuery(sql_get_re_num)
                counter = db_counter.results
                db_counter.dbClose()
                if counter != 0:
                    db_updater = DBConn()
                    db_updater.dbConnect()
                    # print counter
                    sql_update_re_num = "UPDATE Gossiping SET first_page = true, relink = %d WHERE pid = \'%s\'" % (counter[0][0], i[
                        0])
                    # print sql_update_re_num
                    db_updater.runUpdate(sql_update_re_num)
                    db_updater.dbClose()
            except:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                print "2nd MySQL DB Error"
except:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    print "1st MySQL DB Error"
