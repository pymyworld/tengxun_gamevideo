# -*- coding: utf-8 -*-
import scrapy
import re
import time
from copy import deepcopy
import json
import urllib.parse
from ..items import GamevideoItem
from ..video_config import special_author, search_keywords
from ..tools import get_game_id
from ..tools import get_picture
from ..tools import deal_status


class TengxunSpider(scrapy.Spider):
    name = 'tengxun'
    custom_settings = {
        'ITEM_PIPELINES': {
            'gamevideo.pipelines.GamevideoPipeline': 100,
        }
    }
    start_urls = []
    platform_name = "腾讯视频"

    def __init__(self):
        super(TengxunSpider, self).__init__()
        self.make_start_urls(special_author, search_keywords)

    def make_start_urls(self, author_urls, keywords):
        for url in author_urls:
            self.start_urls.append(url)
        for sea in keywords:
            url = "https://v.qq.com/x/search/?q={}&stag=3&cur=1&cxt=tabid%3D0%26sort%3D1%26pubfilter%3D0%26duration%3D0".format(sea)
            self.start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            if url.find('vplus') > 0:
                yield scrapy.Request(
                    url,
                    callback=self.parse_vplus,
                )
            if url.find('search') > 0:
                yield scrapy.Request(
                    url,
                    callback=self.parse_search,
                )

    def parse_vplus(self, response):
        '''解析指定url发布者'''
        if deal_status(response):
            return
        item = GamevideoItem()
        uin = re.findall(r"visited_euin : '(.+)',", response.body.decode())[0]
        item["author_name"] = response.xpath("//span[@id='userInfoNick']/text()").extract_first()
        # 头像url
        author_cover = response.xpath("//img[@id='userAvatar']/@src").extract_first()
        video_info_api = "http://c.v.qq.com/vchannelinfo?otype=json&uin={}&qm=1&pagenum=1&num=24&sorttype=0&orderflag=0&callback=jQuery19106612077281826856_1534840687773".format(uin)
        yield scrapy.Request(
            video_info_api,
            callback=self.parse_detail,
            meta={
                "item": deepcopy(item),
                "uin": deepcopy(uin),
                "author_cover": deepcopy(author_cover),
            }
        )

    def parse_detail(self, response):
        '''提取视频信息'''
        if deal_status(response):
            return
        uin = response.meta["uin"]
        item = response.meta["item"]
        author_cover = response.meta["author_cover"]
        code_url = urllib.parse.unquote(response.url)
        page = re.findall(r'&pagenum=(\d+)&', code_url)[0]
        info_dict = json.loads(re.findall(r'jQuery19106612077281826856_1534840687773\((.+)\)', response.body.decode())[0])
        # total_videos = info_dict["vtotal"]
        video_list = info_dict["videolst"]
        try:
            if len(video_list) == 0:
                return
        except TypeError:
            if video_list is None:
                return
        for video in video_list:
            if "-" in video["uploadtime"]:
                item["author_time"] = int(time.mktime(time.strptime(video["uploadtime"], "%Y-%m-%d")))
            else:
                hour = re.findall(r"\d+", video["uploadtime"])[0]
                item["author_time"] = int(time.time()) - int(hour) * 3600
            # 抓取近一个月视频
            if item["author_time"] > int(time.time()) - 33 * 24 * 3600:
                item["title"] = video["title"]
                item["game_id"] = get_game_id(item["title"])
                # 无法获取改视频game_id则放弃
                if item["game_id"] is None:
                    continue
                # 获取头像图片
                item["author_cover"] = get_picture(author_cover)
                item["live_time"] = int(video["duration"].split(":")[0]) * 60 + int(video["duration"].split(":")[1])
                item["live_html"] = video["url"]
                item["source_from"] = self.platform_name
                item["browse_num"] = int(float(video["play_count"].split("万")[0]) * 10000) if "万" in video["play_count"] else int(video["play_count"])
                # 视频封面图url
                cover_name = re.findall(r"^\w+://vpic\.video\.qq\.com/\d+?/(.*?)_160_90_3\.jpg$", video["pic"])[0]
                high_cover = "http://puui.qpic.cn/qqvideo_ori/0/{}_496_280/0".format(cover_name)
                item["cover"] = get_picture(high_cover)
                vid = video["vid"]
                getinfo_api = "http://vv.video.qq.com/getinfo?vids={}&platform=101001&charge=0&otype=json&defn=shd".format(vid)
                yield scrapy.Request(
                    getinfo_api,
                    callback=self.parse_video,
                    meta={
                        "vid": deepcopy(vid),
                        "item": deepcopy(item),
                    }
                )
            else:
                return
        # 下一页
        video_info_api = "http://c.v.qq.com/vchannelinfo?otype=json&uin={}&qm=1&pagenum={}&num=24&sorttype=0&orderflag=0&callback=jQuery19106612077281826856_1534840687773".format(uin, int(page) + 1)
        yield scrapy.Request(
            video_info_api,
            callback=self.parse_detail,
            meta={
                "uin": deepcopy(uin),
                "item": deepcopy(item),
                "author_cover": deepcopy(author_cover),
            }
        )

    def parse_search(self, response):
        '''解析关键字搜索结果'''
        if deal_status(response):
            return
        code_url = urllib.parse.unquote(response.url)
        game_sort = re.findall(r"\?q=(.*?)&", code_url)[0]
        page = re.findall(r"&cur=(\d+)&", code_url)[0]
        item = GamevideoItem()
        div_list = response.xpath("//div[@class='result_item result_item_h _quickopen']")
        for div in div_list:
            # 封面图地址
            cover = "http:" + div.xpath(".//a[@class='figure result_figure']/img/@src").extract_first()
            video_time = div.xpath(".//span[@class='figure_info']/text()").extract_first()
            try:
                item["live_time"] = int(video_time.split(":")[0]) * 3600 + int(video_time.split(":")[1]) * 60 + int(video_time.split(":")[2])
            except ValueError:
                continue
            video_html = div.xpath(".//a[@class='figure result_figure']/@href").extract_first()
            item["live_html"] = video_html
            vid = re.findall(r"\w+://v\.qq\.com/x/page/(.+)\.html", video_html)[0]
            yield scrapy.Request(
                video_html,
                callback=self.parse_html,
                meta={
                    "item": deepcopy(item),
                    "vid": deepcopy(vid),
                    "cover": deepcopy(cover),
                }
            )
        # 下一页
        next_url = "https://v.qq.com/x/search/?q={}&stag=3&cur=1&cxt=tabid%3D0%26sort%3D1%26pubfilter%3D0%26duration%3D0".format(game_sort, int(page) + 1)
        yield scrapy.Request(
            next_url,
            callback=self.parse_search
        )

    def parse_html(self, response):
        '''解析视频页html'''
        if deal_status(response):
            return
        item = response.meta["item"]
        vid = response.meta["vid"]
        cover = response.meta["cover"]
        date = response.xpath("//span[@class='date _date']/text()").extract_first()
        try:
            item["author_time"] = int(time.mktime(time.strptime(date[0: -2], "%Y年%m月%d日")))
        except TypeError as err:
            return
        # 抓取近一个月视频
        if item["author_time"] > int(time.time()) - 60 * 24 * 3600:
            item["title"] = response.xpath("//h1[@class='video_title _video_title']/text()").extract_first().strip()
            item["game_id"] = get_game_id(item["title"])
            # 无法获取改视频game_id则放弃
            if item["game_id"] is None:
                return
            item["author_name"] = response.xpath("//span[@class='user_name']/text()").extract_first()
            author_cover_url = response.xpath("//img[@class='user_avatar']/@src").extract_first()
            if author_cover_url is None:
                return
            if "http" in author_cover_url:
                # 符合抓取标准，在此下载头像
                item["author_cover"] = get_picture(author_cover_url)
            else:
                author_cover = "http:" + author_cover_url
                # 符合抓取标准，在此下载头像
                item["author_cover"] = get_picture(author_cover)
            item["cover"] = get_picture(cover)
            item["source_from"] = self.platform_name
            view = response.xpath("//em[@id='mod_cover_playnum']/text()").extract_first()
            if "." in view:
                if "万" in view:
                    item["browse_num"] = int(float(view.split("万")[0]) * 10000)
                if "亿" in view:
                    item["browse_num"] = int(float(view.split("亿")[0]) * 100000000)
            else:
                item["browse_num"] = int(view)
            getinfo_api = "http://vv.video.qq.com/getinfo?vids={}&platform=101001&charge=0&otype=json&defn=shd".format(vid)
            yield scrapy.Request(
                getinfo_api,
                callback=self.parse_video,
                meta={
                    "vid": deepcopy(vid),
                    "item": deepcopy(item),
                }
            )
        else:
            return

    def parse_video(self, response):
        '''获得视频地址'''
        if deal_status(response):
            return
        item = response.meta["item"]
        vid = response.meta["vid"]
        info_dict = json.loads(re.findall(r'QZOutputJson=(.+);', response.body.decode())[0])
        # 选择清晰度
        fiid_list = list()
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
            item["add_time"] = int(time.time())
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
                item["add_time"] = int(time.time())
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
        item["add_time"] = int(time.time())
        item["update_time"] = int(time.time())
        yield item
