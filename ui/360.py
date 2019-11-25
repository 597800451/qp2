# -*- coding: UTF-8 -*-
import Tkinter as tk
import tkinter.messagebox
import login as loginUi
import ConfigParser as configparser
import base64
from icon import img

class main:
    def __init__(self):
        self.mima = '321'
        self.top = tk.Tk()
        self.top.title('v1.0')
        self.var = tk.StringVar()
        label_pwd = tk.Label(text='密码:')
        self.pwd = tk.Entry()
        label_pwd.grid(row=0, column=0)
        self.pwd.grid(row=0, column=1)
        btn = tk.Button(text="确认", width=10,command=self.subLogin)
        btn.grid(row=0, column=2, columnspan=5)
        self.Config = self.loadConfig()
        if self.Config is None:
            tkinter.messagebox.showinfo('提示', '配置文件读取失败')
            self.top.destroy()
            return

    def loadConfig(self):
        try:
            Config = configparser.ConfigParser()
            s = Config.read("config.ini")
            if len(s) == 0:
                return None
        except Exception,e:
            print e
            return None
        return Config

    def subLogin(self):

        if self.pwd.get() == '':
            return

        if self.pwd.get() == self.mima:
            sss = self.pwd.get()
            self.top.destroy()
            self.login = loginUi.login(str(sss),self.Config)
            self.login.start()
        else:
            tkinter.messagebox.showinfo('提示', '密码错误')

    def start(self):
        try:
            if self.Config.get("set","is_sys_pas").lower() == 'false':
                self.top.destroy()
                self.login = loginUi.login(self.mima, self.Config)
                self.login.start()
                return
        except Exception,e:
            pass
        self.top.mainloop()

if __name__ == '__main__':
    m = main()
    m.start()