import os
import hashlib
import requests
import logging
import time
import datetime
import pymysql
from .settings import picture_path, MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_PASSWD, MYSQL_USER, CHARSET
from .video_config import game_relation


def get_picture(url):
    '''
    将下载的头像保存在www/static/wx下, 分别创建年，月，日目录
    :return:返回图片在项目中所在路径,用于存储数据库
    '''
    root_path = os.path.abspath(os.path.join(os.getcwd(), '../../../'))
    postfix = '.jpg'
    # 年/月/日
    file_path = "{}/{}/{}/{}".format(picture_path, datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
    if not os.path.exists(root_path + "/www" + file_path):
        os.makedirs(root_path + "/www" + file_path)
    file_name = md5_handle(url)
    file = root_path + "/www" + file_path + "/" + file_name + postfix
    with open(file, 'wb') as f:
        try:
            response = requests.get(url, stream=True)
        except Exception as err:
            logging.error("图片下载中服务器断开连接,将再次请求 url:{} error:{}".format(url, err))
            time.sleep(0.5)
            response = requests.get(url, stream=True)
        for block in response.iter_content(3600):
            if not block:
                break
            f.write(block)
    return file_path + "/" + file_name + postfix


def md5_handle(avatar_url):
    '''
    将头像图片url通过md5加密作为图片名
    :return:
    '''
    if avatar_url is not None:
        m = hashlib.md5()
        m.update(avatar_url.encode())
        return m.hexdigest()


def get_game_id(title):
    for game in game_relation:
        if game[0] in title:
            game_id = game[1]
            return game_id
        else:
            pass
    return None


def deal_status(response):
    '''处理4xx状态码'''
    if response.status == 400 or response.status == 403 or response.status == 404:
        logging.error("time:{},status:{},url:{}".format(time_str(), response.status, response.url))
        return True


def time_str():
    '''
    生成时间戳
    :return:
    '''
    times = int(time.time())
    time_local = time.localtime(times)
    date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return date


class Sqlhandle(object):
    def __init__(self):
        dbparams = dict(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            db=MYSQL_DB,
            charset=CHARSET
        )
        self.connect = pymysql.connect(**dbparams)
        # 自动提交
        self.connect.autocommit(1)
        self.cursor = self.connect.cursor()

    def select_id_live_url(self):
        '''
        从dj_wx_video表中查询主播id和live_url
        :return:
        '''
        sql = "SELECT id,live_html FROM dj_wx_video"
        if self.cursor.execute(sql) > 0:
            return self.cursor.fetchall()

    def select_live_html(self, videoid):
        '''
        从dj_wx_video中查询live_html
        :param id:
        :return:
        '''
        sql = "SELECT live_html FROM dj_wx_video WHERE id=%s"
        self.cursor.execute(sql, [videoid])
        return self.cursor.fetchall()


