"""
网易云音乐下载
爬取关键点：
1、搜索歌曲的url：
'http://music.163.com/weapi/cloudsearch/get/web'

2、搜索请求数据
该请求为post请求，请求数据为：
    s：歌曲名称
    limit：搜索数量
    type类型: 单曲(1), 专辑(10), 歌手(100), 歌单(1000), 用户(1002)

    data = {
            's': search_name,
            'offset': str(offset),
            'limit': str(limit),
            'type': str(stype)
        }

3、搜索歌曲post请求内容为md5加密

4、拼接歌曲url:
    "http://music.163.com/song/media/outer/url?id={}.mp3".format(song_id)

"""


import requests
from music_api.netEaseEncode import *


def wangyi_search_api(search_name):
    headler = {"Host": "music.163.com",
       "Referer": "http://music.163.com",
       "Content-Type": "application/x-www-form-urlencoded",
       "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    offset = 0
    limit = 30
    stype = 1

    """
    搜索.
    limit：搜索数量
    type类型: 单曲(1), 专辑(10), 歌手(100), 歌单(1000), 用户(1002)
    2017/7/15更新API.
    """
    url = 'http://music.163.com/weapi/cloudsearch/get/web'
    data = {
        's': search_name,
        'offset': str(offset),
        'limit': str(limit),
        'type': str(stype)
    }

    data = encrypted_request(data)
    # print(data)
    res = requests.post(url, data, headers=headler)  # 进行post请求
    # print(url)
    res.encoding = 'utf-8'
    # print(res.text)
    html = res.text
    keyjs = json.loads(html)
    songlist = keyjs["result"]["songs"]
    song_list_meesage = []
    for song in songlist:
        buf = {}
        buf["song_name"] = song["name"]
        buf["song_user"] = song["ar"][0]["name"]
        buf["song_id"] = song["id"]
        buf["song_time"] = str(int(song["dt"] / 1000 / 60)) + ":" + str(int((song["dt"] / 1000) % 60))
        buf["song_url"] = "http://music.163.com/song/media/outer/url?id={}.mp3".format(buf["song_id"])

        # 去除重复的歌曲
        song_find_flg = 0
        for song_find in song_list_meesage:
            if (song_find["song_name"] == buf["song_name"]) and (song_find["song_user"] == buf["song_user"]):
                song_find_flg = 1

        # 当song_find_flg==1,说明歌曲和列表重复，
        # 当歌曲id数据长度小于10，说明该id异常
        if song_find_flg == 0 and len(str(buf["song_id"])) >= 10:
            song_list_meesage.append(buf)

        # print(buf["song_name"], "  -  ", buf["song_user"], "  -  ", buf["song_time"], "  -  ", buf["song_id"])
        # print(buf["song_url"])
        # print("************************")
    return song_list_meesage
