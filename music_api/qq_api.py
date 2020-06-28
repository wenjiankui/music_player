"""
QQ音乐下载
爬取关键点：
1、搜索歌曲的url：
    song_name：歌曲名
    pagesize：搜索数量
    'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=%d&w=%s' % (pagesize, search_name)

2、获取purl：
    guid = 889024444
    uin = 4250
    songmid：歌曲id号
    'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}' % (
            guid, guid, songmid, uin, uin)

3、拼接歌曲url:
    'http://dl.stream.qqmusic.qq.com/' + purl
"""


import json
import requests

def qq_search_api(search_name):
    pagesize = 30
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=%d&w=%s' % (pagesize, search_name)
    # 搜索音乐
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    # print(url)
    res = requests.get(url, headers=headers)
    html = res.text
    html = html[9:]
    html = html[:-1]
    # 获取songmid
    js = json.loads(html)
    songlist = js['data']['song']['list']
    guid = 889024444
    uin = 4250
    song_list_meesage = []
    for song in songlist:
        buf = {}
        # print(song)
        buf["song_name"] = song['songname']
        buf["song_user"] = song['singer'][0]['name']
        buf["song_time"] = str(int(int(song["interval"]) / 60)) + ":" + str(int(int(song["interval"]) % 60))

        buf["song_id"] = song['songmid']

        songmid = song['songmid']
        name = song['songname']
        # self.sl.append((name, songmid))

        # print('获取成功songmid')

        keyUrl = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}' % (
            guid, guid, songmid, uin, uin)
        res = requests.get(keyUrl, headers=headers)
        # print(keyUrl)
        # print(res.text)
        html = res.text
        keyjs = json.loads(html)
        purl = keyjs['req_0']['data']['midurlinfo'][0]['purl']
        # 拼凑资源url
        url = 'http://dl.stream.qqmusic.qq.com/' + purl

        buf["song_url"] = url

        # 去除重复的歌曲
        song_find_flg = 0
        for song_find in song_list_meesage:
            if (song_find["song_name"] == buf["song_name"]) and (song_find["song_user"] == buf["song_user"]):
                song_find_flg = 1

        # 当song_find_flg==1,说明歌曲和列表重复，
        # 当歌曲purl数据长度小于1，说明该url异常
        if song_find_flg == 0 and len(purl) > 1:
            song_list_meesage.append(buf)

        # print(buf["song_name"] + " - " + buf["song_user"] + " - " + buf["song_time"] + " - " + buf["song_id"])
        # print(url)
        # print("************************")
    return song_list_meesage
