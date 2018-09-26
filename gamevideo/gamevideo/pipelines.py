# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymysql
import logging
from .tools import time_str
from twisted.enterprise import adbapi


class GamevideoPipeline(object):
    def __init__(self, dbpool, cursor):
        self.start_time = 0
        self.dbpool = dbpool
        self.cursor = cursor
        self.insert_list = list()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['CHARSET']
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        connect = pymysql.connect(**dbparams)
        connect.autocommit(1)
        cursor = connect.cursor()
        return cls(dbpool, cursor)

    def open_spider(self, spider):
        self.start_time = int(time.time())

    def process_item(self, item, spider):
        select = self.select_video(item)
        if select == 0:
            self.insert_list.append(self.make_data(item))
        return item

    def close_spider(self, spider):
        '''
        计算运行时长
        :param spider:
        :return:
        '''
        self.insert_all()
        final_time = int(time.time())
        cost_time = final_time - self.start_time
        logging.error("-*spider:tengxun  cost_time:{}s*-".format(cost_time))

    def insert_all(self):
        '''将insert_list中数据通过全列多行插入存入数据库'''
        sql_str = str()
        if len(self.insert_list) > 0:
            for i in self.insert_list:
                sql_str += i
            sql = "INSERT INTO dj_wx_video (game_id,title,cover,live_url,live_time,author_name,author_cover,author_time,source_from,browse_num,add_time,update_time,live_html) VALUES %s" % sql_str
            sql_result = sql.rstrip(',')
            self.cursor.execute(sql_result)

    def select_video(self, item):
        sql = "SELECT id FROM dj_wx_video WHERE title=%s AND author_name=%s"
        result = self.cursor.execute(sql, [item["title"], item["author_name"]])
        return result

    def make_data(self, item):
        '''构造数据字符串'''
        data_str = "({},'{}','{}','{}',{},'{}','{}',{},'{}',{},{},{},'{}'),".format(int(item["game_id"]), item["title"], item["cover"], item["live_url"], int(item["live_time"]), item["author_name"], item["author_cover"], int(item["author_time"]), item["source_from"], int(item["browse_num"]), item["add_time"], item["update_time"], item["live_html"])
        return data_str


class Tx_updatePipeline(object):
    def __init__(self, dbpool, cursor):
        self.start_time = 0
        self.dbpool = dbpool
        self.cursor = cursor

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['CHARSET']
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        connect = pymysql.connect(**dbparams)
        connect.autocommit(1)
        cursor = connect.cursor()
        return cls(dbpool, cursor)

    def open_spider(self, spider):
        self.start_time = int(time.time())

    def process_item(self, item, spider):
        if self.compare_live_url(item):
            self.dbpool.runInteraction(self.update_live_url, item)
            logging.error("id:{} 已更新live_url,更新时间为{}".format(int(item["video_id"]), time_str()))

    def close_spider(self, spider):
        '''
        计算运行时长
        :param spider:
        :return:
        '''
        final_time = int(time.time())
        cost_time = final_time - self.start_time
        logging.error("-*spider:tx_update  cost_time:{}s*-".format(cost_time))

    def update_live_url(self, cursor, item):
        sql = "UPDATE dj_wx_video SET live_url=%s,update_time=%s WHERE id=%s"
        cursor.execute(sql, [item["live_url"], item["update_time"], int(item["video_id"])])

    def compare_live_url(self, item):
        sql = "SELECT live_url FROM dj_wx_video WHERE id=%s"
        self.cursor.execute(sql, [item["video_id"]])
        result = self.cursor.fetchall()
        if item["live_url"] == result[0][0]:
            return False
        else:
            return True



