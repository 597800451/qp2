# -*- coding: UTF-8 -*-
import requests

class main:
    def __init__(self):
        self.loginUrl = 'https://198.25.100.168:8088/login.do'
        self.qianPiaoUrl = 'https://198.25.100.168:8088/ygt/lcbl/workData.sdo?limit=10&i_sort_sql=id&i_cylx=11&dblyw_sum'
        self.req = requests.Session()

    def start(self):
        self.login()
        self.qianPiao()

    def login(self):
        loginData = {}
        loginData['validate'] = 'login'
        loginData['userId'] = '999496'
        loginData['pass'] = 'Xy666666'
        self.req.get(self.loginUrl,params=loginData,verify=False)

    def qianPiao(self):
        postData = {}
        postData['limit'] = 10
        postData['i_sort_sql'] = 'id'
        postData['i_cylx'] = 11
        postData['dblyw_sum'] = ''
        content = self.req.post(self.qianPiaoUrl,data = postData)
        print content.text

if __name__ == '__main__':
    m = main()
    m.start()