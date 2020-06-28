"""
虾米音乐下载
爬取关键点：
1、搜索歌曲的url：
    keyword：歌曲名
    'http://api.xiami.com/web?v=2.0&app_key=1&key=' + keyword + '&page=1&limit=50&_ksTS=1459930568781_153&callback=jsonp154' + '&r=search/songs'

"""

import json
import requests
from urllib.parse import quote
import urllib


def xiami_search_api(search_name):
    pagesize = "30"  # 请求数目
    headers = {"authority": "www.xiami.com",
               "scheme": "https",
               "accept": "application/json, text/plain, */*",
               "accept-encoding": "gzip, deflate, br",
               "accept-language": "zh-CN,zh;q=0.9",
               "cookie": "xmgid=2fb3da31-5650-4167-bc17-bc17366d210f; xm_sg_tk=8c15ddd5772e0c47d8fd1d31034a2ebf_1592310423806; xm_sg_tk.sig=AUnNFtbLn9qDcPn2m7QUWi5xJaBKdTaYrIH8uwgMFxs; __guid=26329787.2847437516329959000.1592310421342.4805; _uab_collina=159231042347303998891053; cna=YZf7FqAiPRICAXtiXnKvk7F9; _xm_umtoken=TCA834ABD5B0154A250025BEAD25CD0521053B1157443C2FC1502C8FBDC; xm_traceid=0b0fb46115923109378898597e30a6; xm_oauth_state=9b6aaf359d0da6b07ce896ce02cfd582; monitor_count=5; _xm_cf_=65XgLFhm99vnK305UdwtugIG; l=eB_rvfNqQ8gbqiz6KO5wnurza77tiQRfGsPzaNbMiInca6KAwFoj4NQDX839kdtjgtfA5eKzYAkGMRevWzaLRx1byIskP35Yaxv9-; isg=BO7uP6ADPDFIlkhV8rqgp-kiP0Sw77Lp18eeohi13_GM-4pVgX2t-Qe9s2cXI6oB",
               "referer": "https://www.xiami.com/song",
               "sec-fetch-mode": "cors",
               "sec-fetch-site": "same-origin",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    keyword = urllib.parse.quote(search_name.encode("utf-8"))
    url = 'http://api.xiami.com/web?v=2.0&app_key=1&key=' + keyword + '&page=1&limit=50&_ksTS=1459930568781_153&callback=jsonp154' + '&r=search/songs'
    # print(url)
    res = requests.get(url, headers=headers)

    # print(url)
    res.encoding = 'utf-8'
    response = res.text
    # print(response)
    response = json.loads(response[len('jsonp154('):-len(')')])
    # 修改下返回的信息，与之前的网易云对应，这样就不用修改太多即可做扩展。
    data = response['data']
    # print(data)
    songs = data['songs']
    song_list_meesage = []
    # 遍历所有歌曲
    for item in songs:
        buf = {}
        buf["song_name"] = item["song_name"]
        buf["song_user"] = item["artist_name"]
        buf["song_time"] = ""
        buf["song_url"] = item["listen_file"]

        # 去除重复的歌曲
        song_find_flg = 0
        for song_find in song_list_meesage:
            if (song_find["song_name"] == buf["song_name"]) and (song_find["song_user"] == buf["song_user"]):
                song_find_flg = 1

        if song_find_flg == 0 and len(buf["song_url"]) != 0:
            song_list_meesage.append(buf)
        # print(buf["song_name"], "  -  ", buf["song_user"], "  -  ", buf["song_time"])
        # print(buf["song_url"])
        # print("************************")
    return song_list_meesage
