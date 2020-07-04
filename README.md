# music_player
python爬取：网易云，QQ，酷狗，酷我，咪咕，虾米，千千静听七大音乐播放器平台

## 系统环境

python3.7

Windows10x64

火狐浏览器（可以不装）

## 文件结构分析

main.py

主文件，程序入口文件，

包含以下内容：

​	1、qt界面调用

​	2、界面控件设置相关属性，并链接槽函数

​	3、软件调用逻辑实现

main.ui（由QT界面生成软件：”designer.exe“ 生成的界面文件）

main_ui.py（由 “main.ui” 文件转化为python文件）

music_api 文件夹（各个音乐平台爬取接口）

​	kugou_api.p（酷狗音乐爬取接口）

​	kuwo_api.py（酷我音乐爬取接口）

​	migu_api.py（咪咕音乐爬取接口）

​	wangyi_api.py（网易云音乐爬取接口）

​	netEaseEncode.py（网易云爬取所需解密算法）

​	qianqian_api.py（千千静听音乐爬取接口）

​	xiami_api.py（虾米音乐爬取接口）

dist 文件夹（编译成功的软件，可执行程序）



## python模块安装

```python
pip install selenium	# 自动化测试，用于启动狐火浏览器
pip install requests	# 网络请求
pip install lxml		# 解析html字段
pip install urllib3		# 网络解析
pip install mp3play		# 音乐播放器
pip install threading	# 创建线程
pip install PyQt5		# 调用qt界面
pip install PyQt5-tools	# qt界面附带工具
pip install pyinstaller	# 将python文件打包为.exe可执行文件

```

## 说明

![](C:\Users\wjk\Desktop\360截图18750813657163.png)

默认情况下网易云，QQ，酷狗，酷我，前四个播放平台的歌曲可在线播放，剩余三个平台只能下载。

如果想要所有平台都支持在线播放，则需要下载火狐浏览器和对应的火狐浏览器驱动，

注意：需要将狐火浏览器的驱动的路径添加至系统环境变量中

火狐驱动下载地址：https://github-production-release-asset-2e65be.s3.amazonaws.com/25354393/fb04d600-ecd8-11e9-8592-0da58c43e5b2?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20200701%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20200701T102438Z&X-Amz-Expires=300&X-Amz-Signature=011c441657edca5dfd77f9a057ac0efc87e91f2a94847c48258aa10988d0598d&X-Amz-SignedHeaders=host&actor_id=36623519&repo_id=25354393&response-content-disposition=attachment%3B%20filename%3Dgeckodriver-v0.26.0-win64.zip&response-content-type=application%2Foctet-stream

火狐浏览器自己去应用商店下载就好



对爬取过程说明博客：https://blog.csdn.net/qq_39025957/article/details/107022000