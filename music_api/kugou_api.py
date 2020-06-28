"""
酷狗音乐下载
爬取关键点：
1、搜索歌曲的url：
    song_name：歌曲名
    pagesize：搜索数量
    'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240251602301830425_1548735800928&keyword=%s&page=1&pagesize=%s&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1548735800930' % (
        song_name, pagesize)

2、获取下载歌曲的url：
    FileHash：歌曲对应的hash值
    AlbumID：歌曲对应的id值
    'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191010559973368921649_1548736071852&hash=%s&album_id=%s&_=1548736071853' % (
            FileHash, AlbumID)
"""

from tkinter import *
import json
import requests

def kugou_search_api(song_name):
    pagesize = "30"  # 请求数目
    url = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240251602301830425_1548735800928&keyword=%s&page=1&pagesize=%s&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1548735800930' % (
    song_name, pagesize)
    # print(url)
    headler = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "kg_mid=5eab361f4c02763524dbcb955e3844ba; kg_dfid=07pqXv4Y5NDz0msijF1g5C5k; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1590930321,1591532213; __guid=14639665.3162452066454564400.1591534330776.4563; monitor_count=20",
        "if-modified-since": "Mon, 08 Jun 2020 12:15:34 GMT",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    res = requests.get(url, headers=headler)  # 进行get请求
    # print(res.text)
    # 需要注意一点，返回的数据并不是真正的json格式，前后有那个多余字符串需要用正则表达式去掉,只要大括号{}包着的内容
    # json.loads就是将json数据转为python字典的函数
    res = json.loads(re.match(".*?({.*}).*", res.text, re.S).group(1))

    list = res['data']['lists']  # 这个就是歌曲列表
    # print(list)
    # 建立List存放歌曲列表信息，将这个歌曲列表输出，别的程序就可以直接调用
    song_list_meesage = []

    # for循环遍历列表得到每首单曲的信息
    for item in list:
        buf = {}
        # 将列表每项的item['FileHash'],item['AlnbumID']拼接请求url2
        url2 = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191010559973368921649_1548736071852&hash=%s&album_id=%s&_=1548736071853' % (
        item['FileHash'], item['AlbumID'])
        # print(url2)
        headler = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, braccept-language: zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "kg_mid=5eab361f4c02763524dbcb955e3844ba; kg_dfid=07pqXv4Y5NDz0msijF1g5C5k; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1590930321,1591532213; __guid=14639665.3162452066454564400.1591534330776.4563; monitor_count=24",
            "pragma": "no-cache",
            "referer": "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191010559973368921649_1548736071852&hash=B5A2D566C9DE70422F5E5E7203054219&album_id=6960309&_=1548736071853",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

        res2 = requests.get(url2, headers=headler)
        # print(res2.text())
        res2 = json.loads(re.match(".*?({.*}).*", res2.text).group(1))['data']  # 同样需要用正则处理一下才为json格式,再转为字典

        buf["song_name"] = res2['song_name']
        buf["song_user"] = res2['author_name']
        buf["song_time"] = str(int(int(res2["timelength"])/1000/60)) + ":" + str(int(int(res2["timelength"])/1000%60))
        buf["song_url"] = res2['play_url']

        # 去除重复的歌曲
        song_find_flg = 0
        for song_find in song_list_meesage:
            if (song_find["song_name"] == buf["song_name"]) and (song_find["song_user"] == buf["song_user"]):
                song_find_flg = 1

        # 当song_find_flg==1,说明歌曲和列表重复，
        # 当歌曲url数据长度等于0，说明该id异常
        if song_find_flg == 0 and len(buf["song_url"]) != 0:
            song_list_meesage.append(buf)

        # print(buf["song_name"] + " - " + buf["song_user"] + " - " + buf["song_time"])
        # print(url)
        # print("************************")

    return song_list_meesage







