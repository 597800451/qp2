import hashlib
from datetime import datetime

class test:
    def __init__(self):
        pass

def getCont (username,paw):
    count = 0
    while True:
        s = username + paw + str(count)
        x = hashlib.sha256(s)
        if x.hexdigest()[:4] == '0000':
            y = hashlib.sha256(s)
            if y.hexdigest()[4:8] == '0000':
                break
        count = count + 1
    return count

if __name__ == '__main__':

    username = 'zongdai1'
    paw = "aa123456"
    c = 0
    s = 0
    while True:
        c = c+1
        paw = paw + str(c)
        a = datetime.now()
        count = getCont(username, paw)
        b = datetime.now()
        print count
        t = (b-a).microseconds/1000
        print t
        s = s + t
        if c == 100:
            break

    print 'avg = ' + str(s/c)