#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import jieba
import re
import operator
import os
import traceback
import sys
import json
from db_helper import DBConn

dir = os.path.abspath('../ptt_mysql_scrapy/ptt/jieba_dict')
jieba.load_userdict(str(dir) + '/dict.txt')
jieba.load_userdict(str(dir) + '/taiwan_name.txt')
jieba.load_userdict(str(dir) + '/taiwan_actor.txt')
jieba.load_userdict(str(dir) + '/av.txt')
jieba.load_userdict(str(dir) + '/ptt_words.txt')
jieba.load_userdict(str(dir) + '/usa_name.txt')

class JiebaCounter():

    @staticmethod
    def countFrequence(data, hash):
        data = re.sub(
            "[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", data).replace("""

""", '').replace('\n', '')
        tt = jieba.cut(data, cut_all=True)
        # hassoh = {}
        for item in tt:
            if item in hash and len(item) > 1:
                hash[item] += 1
            else:
                hash[item] = 1

        return sorted(hash.items(), key=operator.itemgetter(1), reverse=True)


try:
    dbuse = DBConn()
    dbuse.dbConnect()
    sql = "SELECT * FROM Content"
    dbuse.runQuery(sql)
    result = dbuse.results
    dbuse.dbClose()
except:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    print "MySQL DB Error"



for record in result:
    content_hash = {}
    content_seg = r''.join(json.dumps(JiebaCounter.countFrequence(record[1], content_hash)).decode('unicode-escape'))
    try:
        sql = """Update Gossiping Set content_keywords = '%s' Where pid = "%s\";""" % (
            content_seg, record[0])
        db2 = DBConn()
        db2.dbConnect()
        db2.runUpdate(sql)
        print sql
    except:
        print sql
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
