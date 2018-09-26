# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GamevideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_id = scrapy.Field()    # 游戏分类
    title = scrapy.Field()      # 视频标题
    cover = scrapy.Field()  # 视频封面图
    live_url = scrapy.Field()  # 视频源地址
    live_time = scrapy.Field()      # 视频播放时长
    live_html = scrapy.Field()      # 视频播放页html
    author_name = scrapy.Field()    # 发布者名称
    author_cover = scrapy.Field()   # 发布者头像
    author_time = scrapy.Field()    # 发布时间
    source_from = scrapy.Field()    # 视频所属网站
    browse_num = scrapy.Field()     # 视频浏览数
    add_time = scrapy.Field()   # 添加时间
    update_time = scrapy.Field()    # 更新时间


class Tx_updateItem(scrapy.Item):
    live_url = scrapy.Field()
    video_id = scrapy.Field()
    update_time = scrapy.Field()


