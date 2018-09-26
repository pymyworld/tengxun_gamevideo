# 视频所属游戏分类,指定发布者抓取,腾讯视频搜索关键字 均由该文件配置


# 游戏id
lol = 1     # 英雄联盟
pubg = 11921    # 绝地求生
gok = 55    # 王者荣耀
hs = 13     # 炉石传说
mc = 41     # 我的世界
cjzc = 11922    # 刺激战场
war3 = 31   # 魔兽世界
gamenews = 11923    # 游戏资讯

# 通过title判断游戏分类
game_relation = [
    ['英雄联盟', lol],
    ['LOL', lol],
    ['lol', lol],
    ['起小点', lol],
    ['LPL', lol],
    ['长歌', lol],
    ['青铜', lol],
    ['大神怎么玩', lol],
    ['质量王者局', lol],
    ['秀你一脸', lol],
    ['徐老师', lol],
    ['小苍第一视角', lol],
    ['Miss排位日记', lol],
    ['黑白', lol],
    ['骚男', lol],
    ['神超', lol],
    ['大司马', lol],
    ['Faker', lol],
    ['UZI', lol],
    ['Uzi', lol],
    ['RNG', lol],
    ['S8', lol],
    ['青蛙', lol],
    ['毒纪', lol],
    ['每日撸报', lol],
    ['联盟三分半', lol],
    ['联盟时刻', lol],
    ['刺激战场', cjzc],
    ['大神请带我吃鸡', cjzc],
    ['出击生存手册', cjzc],
    ['Miss吃鸡日记', pubg],
    ['绝地求生', pubg],
    ['吃鸡', pubg],
    ['是大腿', pubg],
    ['求生', pubg],
    ['绝地', pubg],
    ['韦神', pubg],
    ['王者荣耀', gok],
    ['我的世界', mc],
    ['炉石传说', hs],
    ['炉石', hs],
    ['王者TOP10', gok],
    ['王者急诊室', gok],
    ['神探苍英雄计谋', gok],
    ['神探苍', lol],
    ['鱼计可施', gok],
    ['百星王者带你飞', gok],
    ['峡谷情报局', gok],
    ['零度王者视角', gok],
    ['天下王者', gok],
    ['上分拍档', gok],
    ['一鹿上王者', gok],
    ['版本你造吗', gok],
    ['借题FA挥', hs],
    ['FA主播粗事了', hs],
    ['魔兽世界', war3],
    ['魔兽RPG', war3],
    ['STN', gamenews],
    ['屎O说', gamenews],
    ['屎屎看', gamenews],
    ['玩者世界', gamenews],
    ['屌德斯', gamenews],
    ['小格解说', gamenews],
]

# 腾讯视频特定发布者url
special_author = [
    'http://v.qq.com/vplus/changge/videos',     # 起小点系列
    'http://v.qq.com/vplus/silenceob/videos',    # 大神怎么玩
    'http://v.qq.com/vplus/ruofeng/videos',      # 若风
    'http://v.qq.com/vplus/jiumeng/videos',     # 旧梦视频
    'http://v.qq.com/vplus/xsd/videos',         # 小数点解说
    'http://v.qq.com/vplus/3a06efa9725ba03e7a828772ba0710bd/videos',     # 求生是大腿
    'http://v.qq.com/vplus/57aa480bdf3ad65667d5bd9617482a49/videos',     # 大神秀
    'http://v.qq.com/vplus/579484bf7286c0818fdc29f30384c9b3/videos',     # 火焰解说
    'http://v.qq.com/vplus/507bd1ce7c27e09da0b6c87bb849e22c/videos',     # 徐老师视频
    'http://v.qq.com/vplus/ttkapai/videos',     # 天天卡牌
    'http://v.qq.com/vplus/86dd2ddf04d395b0a6cc1771221b2ef5/videos',     # 酱妹说游戏
    'http://v.qq.com/vplus/bd2ba35924de9df628019ebd7c7bd47c/videos',        # 王者荣耀好好笑
    'http://v.qq.com/vplus/9b52679cc868309cdef1e7c7ee68744c/videos',        # 王者荣耀小药店
    'http://v.qq.com/vplus/eca723ab5fa7a7ba/videos',     # 骚白
    'http://v.qq.com/vplus/wangzherongyao/videos',      # 王者荣耀团
    'http://v.qq.com/vplus/6cfb67b337ee1126bafef9e42a504593/videos',    # 虎牙心态
    'http://v.qq.com/vplus/d73f6a7c078c7954bcfe344f11a106c5/videos',    # 韩跑跑
    'http://v.qq.com/vplus/2477eef64e4057e967d5bd9617482a49/videos',    # 王者荣耀梦泪
    'http://v.qq.com/vplus/bd91e789be690a85a6cc1771221b2ef5/videos',    # 王者荣耀职业联赛
    'http://v.qq.com/vplus/45b7c996bfcb9326f120dc8a37aa61aa/videos',    # 王者荣耀小饭堂
    'http://v.qq.com/vplus/4dc182b33ea172527afa2888d66bd01c/videos',    # 银河无极限
    'http://v.qq.com/vplus/fallenangel/videos',     # fallenangle
    'http://v.qq.com/vplus/dahaitv/videos',     # 大海解说
    'http://v.qq.com/vplus/nickgame/videos',    # 晓丁解说
    'http://v.qq.com/vplus/xuewucrazy/videos',      # 血舞crazy
    'http://v.qq.com/vplus/xiusejieshuo/videos',    # 秀色解说
    'http://v.qq.com/vplus/2323a420e8dfca4be370ba49c9e883e0/videos',    # 板娘小薇
    'http://v.qq.com/vplus/7d221a9e2391d488b865a967fcf9e3f7/videos',    # 少云解说
    'http://v.qq.com/vplus/xinbada/videos',     # 辛巴达解说
    'http://v.qq.com/vplus/7e81d6ce8b7c6c96e59d64df08a6d68f/videos',    # 大神请带我吃鸡
    'http://v.qq.com/vplus/f5653964b8e77b946790f8db904e73a1/videos',    # 火尘君
    'http://v.qq.com/vplus/da24da4c1a8f947d923e3b7fce6a6c54/videos',    # 燃茶哥哥
    'http://v.qq.com/vplus/b347c20cf73ab947a3943dada1d257fb/videos',    # 刺激战场情报局
    'http://v.qq.com/vplus/emo/videos',     # 主播真扯淡
    # 'http://v.qq.com/vplus/913fab5b999a7bd5def1e7c7ee68744c/videos',    # 冰糖解说
    # 'http://v.qq.com/vplus/lion/videos',    # 大帝解说
    # 'http://v.qq.com/vplus/4730ecc702c36c6e6f356522325b0902/videos',    # xiaoy解说
    'http://v.qq.com/vplus/stanleyreport/videos',   # 史丹利快报
    'http://v.qq.com/vplus/7bc0fed8fb7e0585def1e7c7ee68744c/videos',    # 玩者世界
    'http://v.qq.com/vplus/gamesdaily/videos',      # 每日游报
    'http://v.qq.com/vplus/diaodesi/videos',        # 屌得斯
    'http://v.qq.com/vplus/eddc1e133df98a89e59d64df08a6d68f/videos',    # 鲤鱼ace
    'http://v.qq.com/vplus/7f331426fab834ee6f7512c83666adff/videos',    # 小格解说
    'http://v.qq.com/vplus/70c6604f202d0b00a25e9827b38c171e/videos',    # 苹果牛
    'http://v.qq.com/vplus/xiaocang/videos',    # 小苍
    'http://v.qq.com/vplus/e67cde2df7ec8004f9bb462829b154a5/videos',    # 史莱姆
    'http://v.qq.com/vplus/c5f7fcb494f0dce064caa14b2714e050/videos',    # 韦神
    'http://v.qq.com/vplus/miss/videos',    # miss
    'http://v.qq.com/vplus/1f17fe1ae143a041d5b0b89a1ce27006/videos',    # 企鹅电竞小浪浪
    'http://v.qq.com/vplus/d235c7af3e1e2738def1e7c7ee68744c/videos',    # Mr.W
    'http://v.qq.com/vplus/ce98b5c116bff5f4d96face787e921b3/videos',    # 飞熊绝地求生
    'http://v.qq.com/vplus/0adccfda765eaee073641ebb97994585/videos',    # 绝地求生阿信解说
    'http://v.qq.com/vplus/171508ff1a5bf6e6d6e00555d6a4fbaa/videos',    # 九阳揽月
    'http://v.qq.com/vplus/eb49ed0dce7a3d730742479233a1d9ba/videos',    # 绝地求生小药店
    'http://v.qq.com/vplus/ae6e9899706773e6def1e7c7ee68744c/videos',    # 蒙面大瞎
    'http://v.qq.com/vplus/c9aa71bdf9eeadc97afa2888d66bd01c/videos',    # 站长解说
    'http://v.qq.com/vplus/54d8ab30eed0ddf9e370ba49c9e883e0/videos',    # 爱电竞i生活
    'http://v.qq.com/vplus/85455d1be5d049613becd2356a3493c4/videos',    # 最强青铜组
    'http://v.qq.com/vplus/e45736e0c262c7c2a0b6c87bb849e22c/videos',    # LOL皮皮虾
    'http://v.qq.com/vplus/99c852b0d88180cc1f15c9a406347560/videos',    # 游云游戏
    'http://v.qq.com/vplus/c67e5aacff73fa5da25e9827b38c171e/videos',    # 纵向观察员
    'http://v.qq.com/vplus/1fd3cfbbf26015b35ee8fc15be93232a/videos',    # 我们的爱情故事
    'http://v.qq.com/vplus/049b1fd7ba478becdef1e7c7ee68744c/videos',    # 世故炎凉
    'http://v.qq.com/vplus/9055cd2545289e3dd6e00555d6a4fbaa/videos',    # 炉石传说爱好者
    'http://v.qq.com/vplus/99cd0a3774dac217e370ba49c9e883e0/videos',    # 游戏小灰说
    'http://v.qq.com/vplus/b67b9496970237ca8a3ed50197ff1f1e/videos',    # 游戏新玩法
    'http://v.qq.com/vplus/4aa27316dfaedb05d8e3af8bd4c40ab9/videos',    # 悟空视角看手游
    'http://v.qq.com/vplus/e58076891e3074798cd6e6189ae90664/videos',    # 猫咪老妖
    'http://v.qq.com/vplus/37d8a063b26d8e678cd6e6189ae90664/videos',    # SharePark
    'http://v.qq.com/vplus/06ded8d58e7a0465e29fcf7d2a3821cf/videos',    # 英雄小黑君
    'http://v.qq.com/vplus/fmsysj/videos',  # 手游视界
    'http://v.qq.com/vplus/1774fa184dfba668610b730147201be9/videos',    # 热门游戏集锦呦
    'http://v.qq.com/vplus/918bfea4bdc7e1d2d198c58fb86eb4dc/videos',    # 王者小皮很皮
    'http://v.qq.com/vplus/647617fe3f39cf2dbcfe344f11a106c5/videos',    # 多玩荣耀
    'http://v.qq.com/vplus/107d7d0cab12ab729e176928bdb00aa9/videos',    # 爱游戏的萌妹纸
    'http://v.qq.com/vplus/meirilubao/videos',      # 每日撸报
]

# 腾讯视频搜索关键词
search_keywords = [
    '英雄联盟',
    'LOL',
    '绝地求生',
    '吃鸡',
    '王者荣耀',
    '炉石传说',
    '我的世界',
    '刺激战场',
    '魔兽世界',
    '游戏资讯',
    # '起小点',
    # '大神怎么玩',
    # '质量王者局',
    # '若风',
    # '旧梦视频',
    # '小数点解说',
    # '求生是大腿',
    # '大神秀',
    # '火焰解说',
    # '徐老师',
    # '天天卡牌',
    # '酱妹说游戏',
    # '王者荣耀好好笑',
    # '王者荣耀小药店',
    # '骚白',
    # 'TGL-王者荣耀团',
    # '虎牙心态',
    # '韩跑跑',
    # '王者荣耀梦泪',
    # '王者荣耀职业联赛',
    # '王者荣耀小饭堂',
    # '银河无极限',
    # '借题FA挥',
    # 'FA主播粗事了',
    # '大海解说',
    # '晓丁解说',
    # '血舞Crazy',
    # '秀色解说',
    # '板娘小薇',
    # '少云解说',
    # '辛巴达解说',
    # '大神请带我吃鸡',
    # '出击生存手册',
    # '燃茶哥哥',
    # '刺激战场情报局',
    # '主播真扯蛋',
    # '冰糖解说',
    # 'LioN大帝',
    # 'xiaoy解说',
    # '史丹利快报',
    # '玩者世界',
    # '每日游报',
    # '屌德斯',
    # '小格解说',
    # '苹果牛',
]