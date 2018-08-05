#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import json
import traceback

from MySQLdb import InternalError, IntegrityError
from twisted.enterprise import adbapi
from hashlib import md5
from scrapy import log
import csv


class WriteToCsv(object):

    def write_to_csv(self, item):
        writer = csv.writer(
            open(item['board'] + ".csv", 'a'), delimiter='\t', lineterminator='\n')
        keys = ['board', 'title', 'date', 'author',
                'author_ip', 'url', 'tag', 'content']
        writer.writerow([item[key] for key in keys])

    def process_item(self, item, spider):
        self.write_to_csv(item)
        return item


class PttStorePipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            #  use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    def _do_upinsert(self, conn, item, spider):
        urlmd5id = self._get_urlmd5id(item)[:30]

        try:
            select_base = "SELECT * FROM `%s` " % (item['board'])
            sql = select_base + "WHERE title like '%s';" % ('%' + item["title"] + '%')
            result = conn.execute(sql)
            item["first_page"] = 1
            item["relink"] = 0
            
            if result != 0:
                print("this series: \" %s \" has in db" % item["title"])
                sql = select_base + "WHERE `ptime` < '%s' and title like '%s';" % (item["date"], '%' + item["title"] + '%')

                result2 = conn.execute(sql)
                if result2 == 0:
                    print(" ---- this new link is not first_page")
                    item["first_page"] = 1
                    sql = """
                    UPDATE `%s` SET first_page = 0, relink = relink + 1 WHERE `ptime` < '%s' and title like '%s';
                    """ % (item['board'],item["date"], '%' + item["title"] + '%')
                    conn.execute(sql)
                else:
                    print(" ---- this new link is the truth first_page")
                    item["first_page"] = 0
                item["relink"] = result
            else:
                print("this is first page")
            x = json.dumps(item["comments"], ensure_ascii=False)
            content_keyword = json.dumps(
                item['content_keywords'], ensure_ascii=False)
            comment_keyword = json.dumps(
                item['comment_keywords'], ensure_ascii=False)
            sql = """
            insert into %s_Content(pid,content)
            values('%s','%s')""" % (item['board'], urlmd5id, ''.join(item["content"]))
            conn.execute(sql)
            sql = """insert into %s_Reply(pid,reply)
            values('%s', '%s');
            """ % (item['board'], urlmd5id, ''.join(x))
            conn.execute(sql)
            sql = """INSERT INTO %s(pid, title, ptime, arthor, ip
            , content_keywords, comment_keywords, push, sheee, arrow,
            first_page, relink )
            Values('%s', '%s', '%s', '%s', '%s', '%s',
            '%s','%d', '%d', '%d', '%d', '%d');
            """ % (item['board'], urlmd5id, item["title"], item["date"], item["author"],
                   item["author_ip"], ''.join(content_keyword),
                   ''.join(comment_keyword), item['push'], item['sheeee'],
                   item['arrow'], item["first_page"], item["relink"])
            conn.execute(sql)
        except IntegrityError as e:
            print("this data has in the db")
        except Exception as e:
            traceback.print_exc()

    def _get_urlmd5id(self, item):
        return md5(item['url'].encode('utf-8')).hexdigest()

    def _handle_error(self, failure, item, spider):
        log.err(failure)








