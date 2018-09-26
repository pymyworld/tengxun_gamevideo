import requests
import re
import time
import json
import pymysql
import logging
import os
import settings as s


sql_select = "SELECT id,live_url,live_html,add_time FROM dj_wx_video WHERE id IN (5696,5695,5694,5693,5692,5691,5690,5689,5688,5687)"
sql_update = "UPDATE dj_wx_video SET live_url=%s WHERE id=%s"


date = time.strftime('%Y-%m-%d', time.localtime(int(time.time())))
time_log = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
LOG_FILE = "./vkey.log"
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


def vaild_judge(video_url, id):
    response = requests.get(video_url)
    if response.status_code == 403:
        logging.error("--id:{} 的live_url的vkey已经失效,失效时间:{}".format(id, time_log))
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


def make_time(add_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(add_time)))


def run():
    start = int(time.time())
    select_list = db_handle("select", sql_select)
    if len(select_list) == 0:
        return
    for i in select_list:
        logging.error("--id:{} 入库时间为{}".format(i[0], make_time(i[3])))
        if not vaild_judge(i[1], i[0]):
            live_url = get_new_url(i[2])
            db_handle("update", sql_update, live_url, i[0])
            logging.error("--id:{} 已更新live_url,更新时间为:{}".format(i[0], time_log))
    logging.error("该脚本运行时间为{}s".format(int(time.time()) - start))


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass

