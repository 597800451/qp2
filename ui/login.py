# -*- coding: UTF-8 -*-
import Tkinter as tk
import requests
import re
import tkinter.messagebox
import qpMain as qd
import base64
from icon import img
import os

class login:
    def __init__(self, subPwd,Config):
        if subPwd != '321':
            return
        self.Config = Config
        self.loginUrl = 'https://198.25.100.168:8088/login.do'
        self.req = requests.Session()
        self.top = tk.Tk()
        tmp = open("ieico.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.top.iconbitmap('.\\ieico.ico')
        os.remove(".\\ieico.ico")
        self.top.title('Internet Explorer')
        if self.Config is None:
            tkinter.messagebox.showinfo('提示', '配置文件读取失败')
            self.top.destroy()
            return
        self.var = tk.StringVar()
        # label_user = tk.Label(text='用户名:')
        label_pwd = tk.Label(text='密码:')
        self.user = tk.Entry(state = 'disabled')
        self.pwd = tk.Entry(show='*')
        # label_user.grid(row=0, column=0)
        # self.user.grid(row=0, column=1)
        label_pwd.grid(row=1, column=0)
        self.pwd.grid(row=1, column=1)
        btn = tk.Button(text="登陆", width=15, command=self.login)
        btn.grid(row=2, column=0, columnspan=5)

    def start(self):
        self.user.config(state=tk.NORMAL)
        self.user.insert(0,"990388")
        self.user.config(state='disabled')
        self.top.mainloop()

    def login(self):
        print 33
        username = self.user.get().replace(" ", "")
        psw = self.pwd.get().replace(" ", "")
        if username == '' or psw == '':
            tkinter.messagebox.showinfo('提示', '请输入户名或密码')
            return
        loginData = {}
        loginData['validate'] = 'login'
        loginData['userId'] = username
        loginData['pass'] = psw
        try:
            content = self.req.get(self.loginUrl, params=loginData, verify=False)
            data = content.content
            if self.getReData("(您输入的用户名或密码有误)", data):
                tkinter.messagebox.showinfo('提示', '您输入的用户名或密码有误')
            else:
                self.top.destroy()
                qpMain = qd.qpMain(self.req, self.Config)
                qpMain.start()
        except Exception,e:
            tkinter.messagebox.showinfo('提示', '网络异常')

    def getReData(self, pattern, data):
        m = re.search(pattern, data)
        if m:
            return m.group(1)
        return None


if __name__ == '__main__':
    m = login()
    m.start()
