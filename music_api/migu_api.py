"""
咪咕音乐下载
爬取关键点：
1、搜索歌曲的url：
    'http://m.music.migu.cn/migu/remoting/scr_search_tag'

2、搜索歌曲url请求参数：
    keyword：歌曲名
    rows：搜索数量
    params = {'rows': pagesize, 'type': 2, 'keyword': key, 'pgc': 1, }

"""

import json
import requests
from urllib.parse import quote
import urllib


def migu_search_api(search_name):
    pagesize = "30"  # 请求数目
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    # res = requests.get(url, headers=headler)   # 进行get请求

    url = 'http://m.music.migu.cn/migu/remoting/scr_search_tag'
    key = urllib.parse.quote(search_name)
    params = {'rows': pagesize, 'type': 2, 'keyword': key, 'pgc': 1, }
    res = requests.get(url, headers=headers, params=params)

    # print(url)
    res.encoding = 'utf-8'
    # print(res.text)
    res = json.loads(res.text)

    res = res["musics"]
    # print(res)
    song_list_meesage = []

    # 遍历所有歌曲
    for item in res:
        buf = {}
        buf["song_name"] = item["songName"]
        buf["song_user"] = item["singerName"]
        buf["song_time"] = ""
        buf["song_url"] = item["mp3"]

        # 去除重复的歌曲
        song_find_flg = 0
        for song_find in song_list_meesage:
            if (song_find["song_name"] == buf["song_name"]) and (
                    song_find["song_user"] == buf["song_user"]):
                song_find_flg = 1

        if song_find_flg == 0 and len(buf["song_url"]) != 0:
            song_list_meesage.append(buf)

        # print(buf["song_name"], "  -  ", buf["song_user"], "  -  ", buf["song_time"])
        # print(buf["song_url"])
        # print("************************")
    return song_list_meesage
