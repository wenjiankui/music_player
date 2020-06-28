"""
酷我音乐下载
爬取关键点：
1、搜索歌曲的url：
    song_name：歌曲名
    pagesize：搜索数量
    'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={0}&pn=1&rn={1}&httpsStatus=1&reqId=d96418b0-adf5-11ea-a73f-a1f5bcc21a3f'.format(
        search_name, pagesize)

2、获取下载歌曲的url：
    song_id：歌曲id号
    "http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web".format(
            song_id)

"""


from tkinter import *
import json
import requests


def kuwo_search_api(search_name):
    pagesize = "10"  # 请求数目
    # 添加提示
    url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={0}&pn=1&rn={1}&httpsStatus=1&reqId=d96418b0-adf5-11ea-a73f-a1f5bcc21a3f'.format(search_name, pagesize)
    # print(url)
    headler = {"Accept": "application/json, text/plain, */*",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Cookie": "__guid=112476674.3591527979254065000.1592106672924.2986; _ga=GA1.2.797505084.1592106674; _gid=GA1.2.45950846.1592106674; _gat=1; radius=14.103.71.201; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1592106674,1592106743,1592108182; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1592108182; uudid=cms5df72a00-3b3e-b4c1-03b5-904d3a4dd6ba; kw_token=E5BXLYPPYS; monitor_count=12",
               "csrf": "E5BXLYPPYS",
               "Host": "www.kuwo.cn",
               "Referer": "http://www.kuwo.cn/search/list?key=".format(search_name),
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    res = requests.get(url, headers=headler)  # 进行get请求
    # print(url)
    res.encoding = 'utf-8'
    res = json.loads(re.match(".*?({.*}).*", res.text, re.S).group(1))
    res = res["data"]["list"]
    # print(res)
    song_list_meesage = []
    i = 0
    # 遍历所有歌曲
    for item in res:
        buf = {}
        buf["song_name"] = item["name"]
        buf["song_user"] = item["artist"]
        buf["song_id"] = item["rid"]
        buf["song_time"] = item["songTimeMinutes"]
        i += 1

        # 以下根据歌曲id获取歌曲url和歌曲播放时间
        get_song_url = "http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web".format(
            buf["song_id"])
        res2 = requests.get(get_song_url)
        # print(res2.text)
        res2 = json.loads(re.match(".*?({.*}).*", res2.text).group(1))  # 同样需要用正则处理一下才为json格式,再转为字典
        # print(res2)
        buf["song_url"] = res2["url"]

        # 去除重复的歌曲
        song_find_flg = 0
        for song_find in song_list_meesage:
            if (song_find["song_name"] == buf["song_name"]) and (
                    song_find["song_user"] == buf["song_user"]):
                song_find_flg = 1

        if song_find_flg == 0 and len(buf["song_url"]) != 0:
            song_list_meesage.append(buf)
        # print(buf["song_name"], "  -  ", buf["song_user"], "  -  ", buf["song_time"], "  -  ", buf["song_id"])
        # print(buf["song_url"])
        # print("************************")
    return song_list_meesage
