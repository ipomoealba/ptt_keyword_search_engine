# -*- coding: utf-8 -*-

# Mongo
import pymongo

# Mysql
import pymysql
import MySQLdb
import MySQLdb.cursors
import json
import codecs

from scrapy import signals
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
from scrapy import log
from ptt import settings
from scrapy.conf import settings
from scrapy.exceptions import DropItem


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PttMongoPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db["post"]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

class MySQLStorePipeline(object):
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
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    def _do_upinsert(self, conn, item, spider):
        urlmd5id = self._get_urlmd5id(item)
        x = json.dumps(item["comments"]).decode('unicode-escape')
        sql = """insert into Gossiping(id, title, ptime, arthor, content, reply,ip)
        values('%s', '%s', '%s', '%s', '%s', '%s', '%s');
        """ % (urlmd5id, item["title"], item["date"], item["author"], item["content"], x,
               item["author_ip"])
        conn.execute(sql)

    def _get_urlmd5id(self, item):
        return md5(item['url']).hexdigest()

    def _handle_error(self, failure, item, spider):
        log.err(failure)
