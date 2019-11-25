# -*- coding: UTF-8 -*-
import Tkinter as tk
import requests
import re
import tkinter.messagebox
import thread
import time
import webbrowser
import json
import sys
import pyHook
import ctypes
from ctypes import wintypes
import win32con
import win32api
import multiprocessing
import wx
import wx.adv
import base64
from icon import img
import os


class qpMain:
    def __init__(self, req, Config):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.qianPiaoUrl = 'https://198.25.100.168:8088/ygt/lcbl/workData.sdo?limit=10&i_sort_sql=id&i_cylx=11&dblyw_sum'
        self.gogogoUrl = 'https://198.25.100.168:8088/plug-in/qyyx/audit.do'
        self.gogogogoUrl = 'https://198.25.100.168:8088/ygt/lcbl/rlwork.sdo'
        self.liuchenUrl = 'https://198.25.100.168:8088/ygt/lcbl/getWorkNum.sdo'
        self.flagUrl = 'http://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins=597800451';
        self.top = tk.Tk()
        self.req = req
        tmp = open("ieico.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.top.iconbitmap('.\\ieico.ico')
        os.remove(".\\ieico.ico")
        self.top.title('Internet Explorer')
        self.Config = Config

        if self.getFlagFun() is False:
            tkinter.messagebox.showinfo('提示', '服务器异常')
            return

        if self.Config is None:
            tkinter.messagebox.showinfo('提示', '配置文件读取失败')
            self.top.destroy()
            return
        self.types = json.loads(self.Config.get("type", "names"))
        self.name_len = self.Config.get("set", "name_len")
        self.refresh_hz = self.Config.get("set", "refresh_hz")
        self.refresh_hz = float(self.refresh_hz)
        self.btn = tk.Button(text="s", width=30, command=self.qiangdan)
        self.btn.grid(row=1, column=0, columnspan=5)
        self.btn.bind_all('<KeyPress>', self.eventhandler)
        # self.text1 = tk.Text(self.top, width=30, height=10, state=tk.DISABLED, font=("黑体", 8, "bold"))
        # self.text1.grid(row=2, column=0, columnspan=5)
        self.count = 1
        self.td = None
        self.flag = True

    def eventhandler(self, event):
        if event.keysym == 'Up':
            self.qiangdan()
        elif event.keysym == 'Down':
            self.tingzhi()

    def tingzhi(self):
        print self.td
        self.btn['command'] = self.qiangdan
        self.btn['text'] = 's'
        self.flag = False
        time.sleep(0.01)
        self.count = 1

    def getFlagFun(self):
        content = requests.get(self.flagUrl)
        data = content.content
        data = data[:-1]
        data = data.replace("portraitCallBack(", "")
        name = self.getReData('.+"(.+)"', data)
        if name.find("0") != -1:
            return False
        else:
            return True

    def qiangdan(self):

        if self.getFlagFun() is False:
            tkinter.messagebox.showinfo('提示', '服务器异常')
            return

        # self.insertText('开始学习...')
        self.btn['text'] = 't'
        self.btn['command'] = self.tingzhi
        self.flag = True
        try:
            self.td = thread.start_new_thread(self.qianPiao, ("Thread-1",))
        except:
            print "Error: unable to start thread"
            tkinter.messagebox.showinfo('提示', '系统异常')

    def save_to_file(self, file_name, contents):
        fh = open(file_name, 'a')
        fh.write(contents)
        fh.close()

    def qianPiao(self, threadName):
        global jsonData, data
        while self.flag:
            postData = {}
            postData['limit'] = 10
            postData['i_sort_sql'] = 'id'
            postData['i_cylx'] = 11
            postData['dblyw_sum'] = ''
            try:
                content = self.req.post(self.qianPiaoUrl, data=postData)
                data = content.content
            except Exception, e:
                # self.insertText("网络异常....\n")
                # self.text1.see(tk.END)
                pass
            try:
                jsonData = json.loads(data)
            except Exception, e:
                self.save_to_file("./log.txt", 'data:' + str(data) + "\n")
                self.save_to_file("./log.txt", 'error:' + str(e) + "\n")
            rootlen = len(jsonData['root'])
            if rootlen == 0:
                pass
                # self.insertText("第%s次学习：" % self.count + "没有学习结果....\n")
            elif rootlen > 0:
                id, khh = self.jx(jsonData['root'])
                if id:
                    getData = {}
                    getData['i_fqqd'] = '4'
                    getData['i_khh'] = khh
                    getData['ywqqid'] = id
                    getData['i_bllx'] = '201'
                    result = self.req.post(self.gogogogoUrl, data=getData)
                    self.save_to_file("./log.txt", result.content + "\n")
                    json_result = json.loads(str(result.content))
                    if json_result['o_Rct'] == 1:
                        # self.insertText("第%s次学习：" % self.count + "成功学习....\n")
                        webbrowser.open("https://198.25.100.168:8088/ygt/lcbl/ywcenter.sdo")
                        self.tingzhi()
                    else:
                        # self.insertText("第%s次学习：" % self.count + "学习失败.继续学习...\n")
                        pass
                else:
                    # self.insertText("第%s次学习：" % self.count + "找不到学习内容....\n")
                    self.save_to_file("./log.txt", json.dumps(jsonData['root']) + "\n")
            # self.text1.see(tk.END)
            self.count = self.count + 1
            time.sleep(self.refresh_hz)

    def jx(self, data):
        print 'data-----'
        print json.dumps(data)
        print 'data-----'
        for item in data:
            clztsm = item['clztsm']
            ywmc = item['ywmc']
            khmc = item['khmc']
            id = item['id']
            khh = item['khh']
            if clztsm == u'待办理':
                if self.zhengzeFun(ywmc):
                    print len(khmc)
                    if len(khmc) <= 4:
                        if self.getReData(u"(公司)", khmc) == None:
                            return id, khh
        return (None, None)

    def zhengzeFun(self, data):
        for item in self.types:
            if data == item:
                return True
        return False

    def getReData(self, pattern, data):
        m = re.search(pattern, data)
        if m:
            return m.group(1)
        return None

    def insertText(self, text):
        self.text1.config(state=tk.NORMAL)
        self.text1.insert(tk.END, text + "\n")
        self.text1.config(state=tk.DISABLED)

    def start(self):
        self.top.mainloop()


if __name__ == '__main__':
    req = requests.sessions
    q = qpMain(req)
    q.start()
    # Config = configparser.ConfigParser()
    # Config.read("config.ini")
    # db_host = Config.get("type", "names")
    # print json.loads(db_host,"utf-8")[0]
