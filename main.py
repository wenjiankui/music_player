"""
音乐下载工具

辰良

1968967834@qq.com

CSDN地址：https://blog.csdn.net/qq_39025957

2020年7月1日

"""


from urllib.request import urlretrieve
from selenium import webdriver

import mp3play
import threading
from PyQt5.QtWidgets import QApplication,QMainWindow,QTableWidgetItem,QAbstractItemView,QPushButton,QHeaderView
from PyQt5.QtCore import pyqtSignal, QObject, Qt
import _thread
from main_ui import *

from music_api.kugou_api import *
from music_api.wangyi_api import *
from music_api.kuwo_api import *
from music_api.migu_api import *
from music_api.qq_api import *
from music_api.qianqian_api import *
from music_api.xiami_api import *


# 信号类，更新QWidget_table
class mysignal(QObject):
    up_widget = pyqtSignal(object, int)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 连接PyQt5界面文件
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 连接界面信号与槽函数
        self.ui.btn_search.clicked.connect(self.btn_search_click)
        self.ui.btn_pause.clicked.connect(self.btn_pause_click)

        # 下载保存的路径为：当前软件运行的目录下的"music"文件中，
        self.down_load_addr = "./music"
        if not os.path.exists(self.down_load_addr):  # 判断一个目录是否存在
            os.makedirs(self.down_load_addr)  # 多层创建目录

        # 搜索结果存放列表，包含歌名，歌手，时长，id, 下载地址
        self.wangyi_song_list_meesage = []
        self.kugou_song_list_meesage = []
        self.kuwo_song_list_meesage = []
        self.migu_song_list_meesage = []
        self.qq_song_list_meesage = []
        self.qianqian_song_list_meesage = []
        self.xiami_song_list_meesage = []
        # 启动搜索标志
        self.wangyi_search_flag = 0
        self.kugou_search_flag = 0
        self.kuwo_search_flag = 0
        self.migu_search_flag = 0
        self.qq_search_flag = 0
        self.qianqian_search_flag = 0
        self.xiami_search_flag = 0
        # 开始写入表格标志
        self.up_table_widget_flag = 0
        self.wangyi_up_table_flag = 0
        self.kugou_up_table_flag = 0
        self.kuwo_up_table_flag = 0
        self.migu_up_table_flag = 0
        self.qq_up_table_flag = 0
        self.qianqian_up_table_flag = 0
        self.xiami_up_table_flag = 0
        # 需要更新的table_widget控件名
        self.table_widget_list = []
        # 当前需要更新的列表行号
        self.run_count = 0
        # 当前是否需要暂停歌曲
        self.btn_pause_flag = 0
        # mp3play播放器
        self.mp3 = mp3play
        # 当前播放的歌曲url
        self.play_song_url = ""
        # 当前播放的歌曲名
        self.play_song_name = ""
        # 切换下一首歌标志
        self.play_flag = 0
        # 当前运行环境是否能使用firfox标志
        self.firfox_flag = 0

        # 循环初始化每一个table_widget控件
        tablewidget_list = [self.ui.tableWidget_wangyi, self.ui.tableWidget_kugou, self.ui.tableWidget_kuwo, self.ui.tableWidget_migu,
                            self.ui.tableWidget_qq, self.ui.tableWidget_qianqian, self.ui.tableWidget_xiami]
        for item in tablewidget_list:
            # 设置4列1行
            item.setColumnCount(4)
            item.setRowCount(0)
            # 设置控件为只读，不允许修改
            item.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # 设置为整行选中方式
            item.setSelectionBehavior(QAbstractItemView.SelectRows)
            # 设置单选目标
            item.setSelectionMode(QAbstractItemView.SingleSelection)
            # 设置不显示格子线
            item.setShowGrid(False)
            # 设置列内容自适应宽度
            item.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            item.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            # 设置双击触发
            item.cellDoubleClicked.connect(self.table_widget_clicked)
            # 设置单击触发
            # item.itemClicked.connect(self.Select)

        # 创建所有线程
        self.build_thread()

        # 实例化触发更新table widget信号
        self.up_table_widget_sig = mysignal()
        self.up_table_widget_sig.up_widget.connect(self.up_table_widget)

        # 创建定时器线程，用于检测更新界面
        self.timer = threading.Timer(1, self.time_up_table_widgt)
        self.timer.start()  # 启动定时器
        # self.timer.cancel()  # 取消定时器

        try:
            # 配置火狐浏览器神隐模式，隐藏浏览器启动
            options = webdriver.FirefoxOptions()
            options.add_argument("-headless")
            # 打开火狐浏览器
            self.driver = webdriver.Firefox(options=options)
            # 请求动态数据
            self.firfox_flag = 1
            print("firfox ok")
        except:
            self.firfox_flag = 0
            print("firfox fail")
        """
        # 设置控件透明度
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.ui.tableWidget_wangyi.setGraphicsEffect(op)
        self.ui.tableWidget_wangyi.setAutoFillBackground(True)
        """


    # 点击暂停按钮触发的槽函数
    def btn_pause_click(self):
        # print("btn_play")
        self.btn_pause_flag = 1

    # 创建所有的线程
    def build_thread(self):
        # 创建一个播放歌曲线程
        try:
            _thread.start_new_thread(self.play_song, ("play_song", 0))
        except:
            print("Error: 无法启动线程")

        # 创建一个网易云搜索线程
        try:
            _thread.start_new_thread(self.wangyi_search_song, ("wangyi_search_song", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个酷狗搜索线程
        try:
            _thread.start_new_thread(self.kugou_search_song, ("kugou_search_song", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个酷我搜索线程
        try:
            _thread.start_new_thread(self.kuwo_search_song, ("kuwo_search_song", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个咪咕搜索线程
        try:
            _thread.start_new_thread(self.migu_search_song, ("migu_search_song", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个QQ搜索线程
        try:
            _thread.start_new_thread(self.qq_search_song, ("qq_search_song", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个千千静听搜索线程
        try:
            _thread.start_new_thread(self.qianqian_search_song, ("qianqian_search_song", 0))
        except:
            print("Error: 无法启动线程")
        # 创建一个虾米搜索线程
        try:
            _thread.start_new_thread(self.xiami_search_song, ("xiami_search_song", 0))
        except:
            print("Error: 无法启动线程")

    # 根据列表行号和控件名称获取对应的歌曲url和歌曲名称
    def object_to_url_name(self, row, table_type):
        table_name = table_type.objectName()
        # print(table_name)
        song_url = ""
        song_name = ""
        if table_name == "tableWidget_wangyi":
            song_url = self.wangyi_song_list_meesage[row]["song_url"]
            song_name = self.wangyi_song_list_meesage[row]["song_name"] + ' - ' + self.wangyi_song_list_meesage[row][
                "song_user"]
        elif table_name == "tableWidget_kugou":
            song_url = self.kugou_song_list_meesage[row]["song_url"]
            song_name = self.kugou_song_list_meesage[row]["song_name"] + ' - ' + self.kugou_song_list_meesage[row][
                "song_user"]
        elif table_name == "tableWidget_kuwo":
            song_url = self.kuwo_song_list_meesage[row]["song_url"]
            song_name = self.kuwo_song_list_meesage[row]["song_name"] + ' - ' + self.kuwo_song_list_meesage[row][
                "song_user"]
        elif table_name == "tableWidget_migu":
            song_url = self.migu_song_list_meesage[row]["song_url"]
            song_name = self.migu_song_list_meesage[row]["song_name"] + ' - ' + self.migu_song_list_meesage[row][
                "song_user"]
        elif table_name == "tableWidget_qq":
            song_url = self.qq_song_list_meesage[row]["song_url"]
            song_name = self.qq_song_list_meesage[row]["song_name"] + ' - ' + self.qq_song_list_meesage[row][
                "song_user"]
        elif table_name == "tableWidget_qianqian":
            song_url = self.qianqian_song_list_meesage[row]["song_url"]
            song_name = self.qianqian_song_list_meesage[row]["song_name"] + ' - ' + \
                        self.qianqian_song_list_meesage[row]["song_user"]
        elif table_name == "tableWidget_xiami":
            song_url = self.xiami_song_list_meesage[row]["song_url"]
            song_name = self.xiami_song_list_meesage[row]["song_name"] + ' - ' + self.xiami_song_list_meesage[row][
                "song_user"]
        else:
            song_name = ""
            song_url = ""
        return song_url, song_name

    """
    点击下载按钮触发的槽函数
    row : 需要下载的歌曲在列表中的行号
    table_type : 下载按钮所在的table_widget
    """
    def btn_down_click(self,row, table_type):
        # print(row)
        # 根据列表行号和控件名称获取对应的歌曲url和歌曲名称
        song_url, song_name = self.object_to_url_name(row, table_type)
        if len(song_name) == 0 or len(song_url) == 0:
            return
        # 创建一个下载线程
        try:
            _thread.start_new_thread(self.down_song, ("down_song", song_name, song_url))
        except:
            print("Error: 无法启动线程")

    """
    table_widget 双击触发的槽函数
    row : 点击的行号
    column : 点击的列号
    """
    def table_widget_clicked(self,row,column):
        # print(row, " : ", column)
        # print(self.sender().objectName())

        # 根据列表行号和控件名称获取对应的歌曲url和歌曲名称
        song_url, song_name = self.object_to_url_name(row, self.sender())
        if len(song_name) == 0 or len(song_url) == 0:
            return
        # 设置当前播放的歌曲地址
        self.play_song_url = song_url
        # 设置当前播放的歌曲名称
        self.play_song_name = song_name
        # 启动播放线程切歌
        self.play_flag = 1

    # 根据搜索的歌曲名称，找到搜索结果
    def btn_search_click(self):
        # 从输入框获取需要搜索的歌曲名
        search_name = self.ui.lineEdit.text()
        if len(search_name) == 0:
            return
        # 添加提示
        self.ui.label.setText("正在搜索: 《{}》...".format(search_name))
        # 参数复位
        self.table_widget_list = []
        self.up_table_widget_flag = 0
        self.wangyi_up_table_flag = 0
        self.kugou_up_table_flag = 0
        self.kuwo_up_table_flag = 0
        self.migu_up_table_flag = 0
        self.qq_up_table_flag = 0
        self.qianqian_up_table_flag = 0
        self.xiami_up_table_flag = 0

        # 启动搜索标志
        self.wangyi_search_flag = 1
        self.kugou_search_flag = 1
        self.kuwo_search_flag = 1
        self.migu_search_flag = 1
        self.qq_search_flag = 1
        self.qianqian_search_flag = 1
        self.xiami_search_flag = 1

    def wangyi_search_song(self, name, age):
        while 1:
            if self.wangyi_search_flag:
                search_name = self.ui.lineEdit.text()
                self.wangyi_song_list_meesage = wangyi_search_api(search_name)
                self.wangyi_search_flag = 0
                self.wangyi_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("网易搜索完成")

    def kugou_search_song(self, name, age):
        while 1:
            if self.kugou_search_flag:
                search_name = self.ui.lineEdit.text()
                self.kugou_song_list_meesage = kugou_search_api(search_name)
                self.kugou_search_flag = 0
                self.kugou_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("酷狗搜索完成")

    def kuwo_search_song(self, name, age):
        while 1:
            if self.kuwo_search_flag:
                search_name = self.ui.lineEdit.text()
                self.kuwo_song_list_meesage = kuwo_search_api(search_name)
                self.kuwo_search_flag = 0
                self.kuwo_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("酷我搜索完成")

    def migu_search_song(self, name, age):
        while 1:
            if self.migu_search_flag:
                search_name = self.ui.lineEdit.text()
                self.migu_song_list_meesage = migu_search_api(search_name)
                self.migu_search_flag = 0
                self.migu_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("咪咕搜索完成")

    def qq_search_song(self, name, age):
        while 1:
            if self.qq_search_flag:
                search_name = self.ui.lineEdit.text()
                self.qq_song_list_meesage = qq_search_api(search_name)
                self.qq_search_flag = 0
                self.qq_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("QQ搜索完成")

    def qianqian_search_song(self, name, age):
        while 1:
            if self.qianqian_search_flag:
                search_name = self.ui.lineEdit.text()
                self.qianqian_song_list_meesage = qinaqian_search_api(search_name)
                self.qianqian_search_flag = 0
                self.qianqian_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("千千搜索完成")

    def xiami_search_song(self, name, age):
        while 1:
            if self.xiami_search_flag:
                search_name = self.ui.lineEdit.text()
                self.xiami_song_list_meesage = xiami_search_api(search_name)
                self.xiami_search_flag = 0
                self.xiami_up_table_flag = 1
                self.up_table_widget_flag = 1
                print("虾米搜索完成")

    """
    根据控件名返回对应的歌曲列表
    table_type : 控件名
    """
    def object_to_song_list(self, table_type):
        # 将table_type 转换为 objectName()
        table_name = table_type.objectName()
        if table_name == "tableWidget_wangyi":
            return self.wangyi_song_list_meesage
        elif table_name == "tableWidget_kugou":
            return self.kugou_song_list_meesage
        elif table_name == "tableWidget_kuwo":
            return self.kuwo_song_list_meesage
        elif table_name == "tableWidget_migu":
            return self.migu_song_list_meesage
        elif table_name == "tableWidget_qq":
            return self.qq_song_list_meesage
        elif table_name == "tableWidget_qianqian":
            return self.qianqian_song_list_meesage
        elif table_name == "tableWidget_xiami":
            return self.xiami_song_list_meesage
        else:
            return ""

    # 定时器触发函数，更新table_widget界面显示
    def time_up_table_widgt(self):
        # 当有搜索完成标志时，向table_widget_list添加对应的控件名，等待歌曲信息写入对应控件
        if self.wangyi_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_wangyi)
            self.wangyi_up_table_flag = 0
        elif self.kugou_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_kugou)
            self.kugou_up_table_flag = 0
        elif self.kuwo_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_kuwo)
            self.kuwo_up_table_flag = 0
        elif self.migu_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_migu)
            self.migu_up_table_flag = 0
        elif self.qq_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_qq)
            self.qq_up_table_flag = 0
        elif self.qianqian_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_qianqian)
            self.qianqian_up_table_flag = 0
        elif self.xiami_up_table_flag:
            self.table_widget_list.append(self.ui.tableWidget_xiami)
            self.xiami_up_table_flag = 0

        # 如果更新table_widget标志和self.table_widget_list列表不为空，则向up_table_widget发送信号
        if self.up_table_widget_flag == 1 and len(self.table_widget_list) != 0:
            # print(self.run_count)
            # 发送更新信号，并附带需要更新的控件名和列表行号
            self.up_table_widget_sig.up_widget.emit(self.table_widget_list[0], self.run_count)

            song_list = self.object_to_song_list(self.table_widget_list[0])
            if self.run_count < len(song_list)-1:
                self.run_count += 1
            else:
                # print(self.table_widget_list)
                self.run_count = 0
                # 如果更新列表不为空，则删除第一个元素
                if len(self.table_widget_list):
                    del self.table_widget_list[0]

                # 如果更新列表不为空，则继续更新下一个控件，否则停止更新
                if len(self.table_widget_list) == 0:
                    self.up_table_widget_flag = 0
                    self.ui.label.setText("搜索完成")
                else:
                    self.up_table_widget_flag = 1

        # print(datetime.datetime.utcnow().strftime('%Y-%m-%d%H:%M:%S'))  # 测试定时器响应时间
        self.timer = threading.Timer(0.3, self.time_up_table_widgt)  # 创建一个定时任务，每0.3秒启动一次
        self.timer.start()  # 启动定时器

    """
    更新table_widget界面显示
    table_type : table_widget控件名
    row : 添加第几行
    """
    def up_table_widget(self, table_type, row):
        self.up_table_widget_flag = 0
        # num = 0
        # table_type.setRowCount(0)
        # table_type.clearContents()
        # print(datetime.datetime.now())

        # 根据要操作的控件名，获取对应的歌曲列表
        song_list = self.object_to_song_list(table_type)
        # 如果歌曲列表为空，说明搜索结果为空，清空该控件，并返回
        if len(song_list) == 0:
            self.up_table_widget_flag = 1
            table_type.setRowCount(0)  # 清空table显示
            return

        # 如果写入的行号大于歌曲列表的的长度，说明该行号不可用，
        if len(song_list) <= row:
            # print(len(song_list), " ： ", row)
            self.up_table_widget_flag = 1
            return

        # 向控件添加一行歌曲信息
        song_list = song_list[row]
        # print(song_list)
        table_type.setRowCount(row + 1)  # 总行数增加1
        table_type.setItem(row, 0, QTableWidgetItem(song_list["song_name"]))
        table_type.setItem(row, 1, QTableWidgetItem(song_list["song_user"]))
        table_type.setItem(row, 2, QTableWidgetItem(song_list["song_time"]))
        btn_down = QPushButton("下载")
        # 将按钮点击事件链接btn_down_click，在点击时，附带row_n, column参数传递，
        btn_down.clicked.connect(lambda state, row_n=row, column=table_type: self.btn_down_click(row_n, column))
        # 将按钮添加至table_widget
        table_type.setCellWidget(row, 3, btn_down)

        self.up_table_widget_flag = 1
        # self.up_table_widget_flag = 0

        # num += 1
        # print(datetime.datetime.now())

    # 播放歌曲线程
    def play_song(self, name, age):
        while 1:
            if self.play_flag:
                song_url = self.play_song_url
                song_name = self.play_song_name
                # 播放当前列表歌曲
                if len(song_url):
                    # 如果当前环境有firfox则使用firfox进行播放，反之则用MP3play
                    if self.firfox_flag:
                        try:
                            self.driver.get(song_url)
                            self.ui.label.setText("正在播放: 《{}》...".format(song_name))
                        except:
                            print("play erro : ", song_url)
                    else:
                        if 'migu' in song_url or'dmhmusic' in song_url or 'xiami' in song_url:
                            pass
                        elif 'qqmusic' in song_url:
                            try:
                                self.mp3 = mp3play.load(song_url + '.mp3')
                                self.mp3.play()
                                self.ui.label.setText("正在播放: 《{}》...".format(song_name))
                            except:
                                print("play erro : ", song_url)
                        else:
                            try:
                                self.mp3 = mp3play.load(song_url)
                                self.mp3.play()
                                self.ui.label.setText("正在播放: 《{}》...".format(song_name))
                            except:
                                print("play erro : ", song_url)
                self.play_flag = 0

            if self.btn_pause_flag == 1:
                if self.firfox_flag:
                    self.driver.get("http://www.baidu.com")
                else:
                    self.mp3.pause()
                self.btn_pause_flag = 0
                self.ui.label.setText("停止播放")

    """
    根据歌曲名和url下载歌曲，每一首歌的下载，都是一个新的线程
    name : 线程名称
    song_name : 歌曲名称
    song_url : 歌曲下载的url
    """
    def down_song(self, name, song_name, song_url):
        if len(song_url) == 0:
            return
        # 文件名中":"属于特殊字符，在文件保存中会出错，将之替换为中文的"："就没问题
        if ":" in song_name:
            song_name = song_name.replace(":", "：")
        if "/" in song_name:
            song_name = song_name.replace("/", "-")
        if "." in song_name:
            song_name = song_name.replace(".", "-")

        print(song_name, " : ", song_url)
        # 添加提示
        self.ui.label.setText("正在下载: 《{}》...".format(song_name))
        # 下载保存
        urlretrieve(song_url, r"{}.mp3".format(self.down_load_addr + '/' + song_name))
        # 添加提示
        self.ui.label.setText("下载完成: 《{}》".format(song_name))

    # 重载键盘回车
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return:
            # print('Space')
            self.btn_search_click()

    # 重载qt窗体关闭函数
    def closeEvent(self, event):
        print("window close")
        # 在关闭窗口前，先关闭浏览器
        if self.firfox_flag:
            self.driver.quit()
        self.close()
        event.accept()
        os._exit(0)


if __name__ == '__main__':
    app = QApplication([])
    stats = MainWindow()
    stats.show()

    sys.exit(app.exec_())


