# music_player
python爬取：网易云，QQ，酷狗，酷我，咪咕，虾米，千千静听七大音乐播放器平台

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

