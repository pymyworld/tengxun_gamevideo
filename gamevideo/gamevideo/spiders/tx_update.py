# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
import logging
from copy import deepcopy
from ..tools import Sqlhandle, deal_status, time_str
from ..items import Tx_updateItem


class TxUpdateSpider(scrapy.Spider):
    name = 'tx_update'
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'gamevideo.pipelines.Tx_updatePipeline': 100,
        }
    }

    def __init__(self):
        super(TxUpdateSpider, self).__init__()
        self.relation = dict()
        self.sql = Sqlhandle()
        self.select_live_url = self.sql.select_id_live_url()
        self.make_start_urls(self.select_live_url)

    def make_start_urls(self, select_live_url):
        for i in select_live_url:
            video_id = i[0]
            try:
                vid = re.findall(r"\w+://v\.qq\.com/x/page/(.+)\.html", i[1])[0]
            except IndexError as err:
                logging.error("id值为{} 未取得vid值 live_html:{} error:{}".format(i[0], i[1], err))
                continue
            getinfo_api = "http://vv.video.qq.com/getinfo?vids={}&platform=101001&charge=0&otype=json&defn=shd".format(vid)
            self.start_urls.append(getinfo_api)
            self.relation[getinfo_api] = video_id

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_video,
                meta={"getinfo_api": deepcopy(url)}
            )

    def parse_video(self, response):
        '''获得视频地址'''
        if deal_status(response):
            return
        getinfo_api = response.meta["getinfo_api"]
        video_id = self.relation[getinfo_api]
        live_html = self.sql.select_live_html(int(video_id))[0][0]
        vid = re.findall(r"\w+://v\.qq\.com/x/page/(.+)\.html", live_html)[0]
        item = Tx_updateItem()
        item["video_id"] = video_id
        info_dict = json.loads(re.findall(r'QZOutputJson=(.+);', response.body.decode())[0])
        # 选择清晰度
        fiid_list = list()
        if info_dict.get("fl") is None:
            logging.error("vid status wrong 视频已下架 id:{} live_html:{} vid:{}".format(video_id, live_html, vid))
            return
        for i in info_dict["fl"]["fi"]:
            fiid_list.append(i["id"])
        if 10701 in fiid_list:  # 超清
            video_api = "http://vv.video.qq.com/getkey?format=10701&otype=json&vt=150&vid={}&ran=0\%2E9477521511726081\\&charge=0&filename={}.p701.1.mp4&platform=11".format(vid, vid)
            yield scrapy.Request(
                video_api,
                callback=self.parse_super,
                meta={
                    "info_dict_1": deepcopy(info_dict),
                    "item": deepcopy(item),
                }
            )
        elif 2 in fiid_list:  # 高清
            video_api = "http://vv.video.qq.com/getkey?format=2&otype=json&vt=150&vid={}&ran=0\%2E9477521511726081\\&charge=0&filename={}.mp4&platform=11".format(vid, vid)
            yield scrapy.Request(
                video_api,
                callback=self.parse_high,
                meta={
                    "info_dict_1": deepcopy(info_dict),
                    "item": deepcopy(item),
                }
            )
        elif 100701 in fiid_list:  # 标清
            video_url = info_dict["vl"]["vi"][0]["ul"]["ui"][0]["url"] + info_dict["vl"]["vi"][0]["fn"] + "?vkey=" + info_dict["vl"]["vi"][0]["fvkey"]
            item["live_url"] = video_url
            item["update_time"] = int(time.time())
            yield item

    def parse_high(self, response):
        '''得到高清地址'''
        if deal_status(response):
            return
        info_dict_1 = response.meta["info_dict_1"]
        item = response.meta["item"]
        info_dict_2 = json.loads(re.findall(r'QZOutputJson=(.+);', response.body.decode())[0])
        url_list = info_dict_1["vl"]["vi"][0]["ul"]["ui"]
        for url in url_list:
            if ".video." in url["url"] or "/video." in url["url"]:
                main_url = url["url"]
                video_url = main_url + info_dict_2["filename"] + "?vkey=" + info_dict_2["key"]
                item["live_url"] = video_url
                item["update_time"] = int(time.time())
                yield item
                break
        # video_url = info_dict_1["vl"]["vi"][0]["ul"]["ui"][0]["url"] + info_dict_2["filename"] + "?vkey=" + info_dict_2["key"]

    def parse_super(self, response):
        '''得到超清地址'''
        if deal_status(response):
            return
        info_dict_1 = response.meta["info_dict_1"]
        item = response.meta["item"]
        info_dict_2 = json.loads(re.findall(r'QZOutputJson=(.+);', response.body.decode())[0])
        video_url = info_dict_1["vl"]["vi"][0]["ul"]["ui"][0]["url"] + info_dict_2["filename"] + "?vkey=" + info_dict_2["key"]
        item["live_url"] = video_url
        item["update_time"] = int(time.time())
        yield item
