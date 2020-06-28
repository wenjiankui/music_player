"""
千千静听音乐下载
千千静听的搜索网站总是容易崩溃，不是爬虫代码问题，
爬取关键点：
1、搜索歌曲的url：
    song_name：歌曲名
    'http://music.taihe.com/search?key={}'.format(search_name)

2、获取下载歌曲的url：
    song_id：歌曲id号
    "http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&songid={}&from=web".format(
            song_id)
"""

import json
import requests
from lxml import etree
from tkinter import *

def qinaqian_search_api(search_name):

    url = 'http://music.taihe.com/search?key={}'.format(search_name)
    # print(url)
    headler = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "BAIDUID=5E197A46D5DE27D129DF8D97C781E2EF:FG=1; BDUSS=VTRUtuSm1yZC1Dc0JEcTM5OEtwTlMtN3MwYTctNHc1cDJBSndMekF0OFFUcGxlSVFBQUFBJCQAAAAAAAAAAAEAAAAoMSKXsrvWqrXAYWJzZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABDBcV4QwXFeM2; __guid=27716768.2450076713623693300.1590930338562.92; radius=14.103.71.201; uudid=cmsaf4cc63d-232a-a7fc-158a-68d3794e55f1; u_login=1; userid=2535600424; u_id=; u_t=; tracesrc=-1%7C%7C-1; Hm_lvt_03ebc396eb9eeb344da124bee12c91fb=1592054566,1592054685; Hm_lvt_d0ad46e4afeacf34cd12de4c9b553aa6=1592054531,1592054684,1592054809,1592094229; log_sid=15920978559335E197A46D5DE27D129DF8D97C781E2EF; Hm_lpvt_d0ad46e4afeacf34cd12de4c9b553aa6=1592097865; u_lo=2; monitor_count=31",
        "Host": "music.taihe.com",
        "Referer": "http://music.taihe.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    try:
        res = requests.get(url, headers=headler)  # 进行get请求
    except:
        print("qianqian get erro")
        return []
    # print(url)
    res.encoding = 'utf-8'
    # print(res.text)

    # 拿到html_str后就可以使用etree.HTML()方法获取html对象，之后就可以使用xpath方法了
    html = etree.HTML(res.text)
    # print(html)
    try:
    # ①获取所有歌曲title，直接定位到标签）
        song_list = html.xpath("//*[@id='result_container']/div/div")
        # print(song_list)

        song_message_list = song_list[0].xpath("//*[@class='song-title']/a/@title")
        song_id_list = song_list[0].xpath("//*[@class='song-title']/a/@data-songdata")
    except:
        print("qianqian search erro")
        return []

    # print(song_message)
    # print(song_id_list)
    song_list_meesage = []
    i = 0
    # 遍历所有歌曲
    for item in song_message_list:
        buf = {}
        buf["song_name"] = item.split("《")[1].split("》")[0]
        buf["song_user"] = item.split("《")[0]
        buf["song_id"] = json.loads(song_id_list[i])["id"]

        i += 1

        # 以下根据歌曲id获取歌曲url和歌曲播放时间
        get_song_url = "http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&songid={}&from=web".format(
            buf["song_id"])
        res2 = requests.get(get_song_url)
        # print(res2.text)
        res2 = json.loads(re.match(".*?({.*}).*", res2.text).group(1))['bitrate']  # 同样需要用正则处理一下才为json格式,再转为字典
        buf["song_time"] = str(int(res2["file_duration"] / 60)) + ":" + str(int(res2["file_duration"] % 60))
        buf["song_url"] = res2["file_link"]

        # 去除重复的歌曲
        song_find_flg = 0
        for song_find in song_list_meesage:
            if (song_find["song_name"] == buf["song_name"]) and (
                    song_find["song_user"] == buf["song_user"]):
                song_find_flg = 1

        # 当song_find_flg==1,说明歌曲和列表重复，
        # 当歌曲url数据长度等于0，说明该歌曲异常
        if song_find_flg == 0 and len(buf["song_url"]) != 0:
            song_list_meesage.append(buf)

        # print(buf["song_name"], "  -  ", buf["song_user"], "  -  ", buf["song_time"], "  -  ", buf["song_id"])
        # print(buf["song_url"])
        # print("************************")
    return song_list_meesage
