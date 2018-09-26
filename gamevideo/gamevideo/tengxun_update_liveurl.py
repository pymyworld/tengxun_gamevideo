# 该脚本单独执行,更新数据库中腾讯视频源地址
import requests
import pymysql
import re
import json
import time
import threading
import logging
import os
import settings as s


sql_select = "SELECT id,live_url,live_html FROM dj_wx_video"
sql_update = "UPDATE dj_wx_video SET live_url=%s WHERE id=%s"

date = time.strftime('%Y-%m-%d', time.localtime(int(time.time())))
LOG_FILE = "./log/tx_update_{}.log".format(date)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s %(filename)s-%(levelname)s:%(message)s",
    filename=os.path.join(os.getcwd(), LOG_FILE),
    filemode="a"
)


def db_handle(form, sql, *args):
    connect = pymysql.connect(
        host=s.MYSQL_HOST,
        port=s.MYSQL_PORT,
        database=s.MYSQL_DB,
        user=s.MYSQL_USER,
        password=s.MYSQL_PASSWD,
        charset=s.CHARSET,
    )
    connect.autocommit(1)
    cursor = connect.cursor()
    if form == 'select':
        cursor.execute(sql)
        return cursor.fetchall()
    if form == 'update':
        cursor.execute(sql, args)
    cursor.close()
    connect.close()


def vaild_judge(video_url):
    response = requests.get(video_url)
    if response.status_code == 403:
        return False
    else:
        return True


def get_new_url(live_html):
    vid = re.findall(r"\w+://v\.qq\.com/x/page/(.+)\.html", live_html)[0]
    getinfo_api = "http://vv.video.qq.com/getinfo?vids={}&platform=101001&charge=0&otype=json&defn=shd".format(vid)
    try:
        res_1 = requests.get(getinfo_api)
    except Exception:
        time.sleep(0.5)
        res_1 = requests.get(getinfo_api)
    info_dict_1 = json.loads(re.findall(r'QZOutputJson=(.+);', res_1.content.decode())[0])
    # 选择清晰度
    fiid_list = list()
    for i in info_dict_1["fl"]["fi"]:
        fiid_list.append(i["id"])
    if 10701 in fiid_list:  # 超清
        video_api = "http://vv.video.qq.com/getkey?format=10701&otype=json&vt=150&vid={}&ran=0\%2E9477521511726081\\&charge=0&filename={}.p701.1.mp4&platform=11".format(vid, vid)
        res_2 = requests.get(video_api)
        info_dict_2 = json.loads(re.findall(r'QZOutputJson=(.+);', res_2.content.decode())[0])
        live_url = info_dict_1["vl"]["vi"][0]["ul"]["ui"][0]["url"] + info_dict_2["filename"] + "?vkey=" + info_dict_2["key"]
        return live_url
    elif 2 in fiid_list:  # 高清
        video_api = "http://vv.video.qq.com/getkey?format=2&otype=json&vt=150&vid={}&ran=0\%2E9477521511726081\\&charge=0&filename={}.mp4&platform=11".format(vid, vid)
        try:
            res_2 = requests.get(video_api)
        except Exception:
            time.sleep(0.5)
            res_2 = requests.get(video_api)
        info_dict_2 = json.loads(re.findall(r'QZOutputJson=(.+);', res_2.content.decode())[0])
        live_url = info_dict_1["vl"]["vi"][0]["ul"]["ui"][0]["url"] + info_dict_2["filename"] + "?vkey=" + info_dict_2["key"]
        return live_url
    elif 100701 in fiid_list:  # 标清
        live_url = info_dict_1["vl"]["vi"][0]["ul"]["ui"][0]["url"] + info_dict_1["vl"]["vi"][0]["fn"] + "?vkey=" + info_dict_1["vl"]["vi"][0]["fvkey"]
        return live_url


def run():
    start = int(time.time())
    connect = pymysql.connect(
        host=s.MYSQL_HOST,
        port=s.MYSQL_PORT,
        database=s.MYSQL_DB,
        user=s.MYSQL_USER,
        password=s.MYSQL_PASSWD,
        charset=s.CHARSET,
    )
    connect.autocommit(1)
    cursor = connect.cursor()
    t = threading.Thread(target=main, args=(cursor,))
    t.start()
    if len(threading.enumerate()) == 0:
        logging.error("运行时间:{}s".format(int(time.time()) - start))


def main(cursor):
    # select_list = db_handle("select", sql_select)
    cursor.execute(sql_select)
    select_list = cursor.fetchall()
    if len(select_list) == 0:
        return
    for i in select_list:
        if not vaild_judge(i[1]):
            live_url = get_new_url(i[2])
            # db_handle("update", sql_update, live_url, i[0])
            cursor.execute(sql_update, [live_url, i[0]])
            logging.error("已更新一条live_url,id为 {}".format(i[0]))


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass
