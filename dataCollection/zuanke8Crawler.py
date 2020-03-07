# -*- coding:utf-8 -*-
import re, sys, time, requests
from UserAgent import getUserAgent
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")

def getContent(baseUrl, pageNum):
    url = baseUrl + "&page=" + pageNum
    s = requests.session()
    s.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 5
    ua = getUserAgent()
    headers = {'User-Agent': ua, 'Referer': 'zuanke8.com', 'Connection': 'keep-alive', 'Host': 'www.zuanke8.com'}
    try:
        r = requests.get(url, timeout = 10, headers=headers)
        return BeautifulSoup(r.content, 'lxml')
    except Exception as e:
        if hasattr(e, "reason"):
            print "Failed:", e.reason
        return None   


def getPosts(content):
    currentTime = time.strftime("%Y-%m-%d-%H-%M")
    posts = content.find_all('tbody',{'id': re.compile("normalthread_*")})
    ret = []
    for post in posts:
        try:
            postId = post.get("id").split("_")[1]
            href = post.find('tr').find('th', class_='new').find('a')['href']
            title = post.find('tr').find('th', class_='new').find('a').get_text().strip().encode('utf-8')
            ret.append([currentTime, postId, title, href])
        except Exception as e:
            pass
    return ret
          

def getThreads(threadUrl, title, idd):
    s = requests.session()
    s.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 5
    ua = getUserAgent()
    headers = {'User-Agent': ua, 'Referer': 'zuanke8.com', 'Connection': 'keep-alive', 'Host': 'www.zuanke8.com'}
    threads = []
    try:
        r = requests.get(threadUrl, timeout = 10, headers=headers)
        content = BeautifulSoup(r.content, 'lxml')
        floors = content.find_all('div', id = re.compile("^post_[0-9]{8}"))
        ret = []
        title2 = floors[0].find('table').find('tr').find('td', class_='plc').find('table').get_text().strip().encode('utf-8').replace("rt", "").replace("\r\n", ", ").replace("\n", ", ").replace("\r", ", ").strip(", , ")
        if title2.startswith(title) and title2.decode('utf-8') >= title.decode('utf-8'):
            title = title2
        threads.append(idd)    
        threads.append(title)
        for floor in floors[1:]:
            reply = floor.find('table').find('tr').find('td', class_='plc').find('table').get_text().strip().encode('utf-8').replace("rt", "").replace("\r\n", ", ").replace("\n", ", ").replace("\r", ", ").strip(", , ")
            tmp = reply.split(", ")
            if tmp[0].find(u'发表于') != -1:
                reply = ", ".join(tmp[2:])
            threads.append(reply)

        if len(floors) == 20:
            r = requests.get(threadUrl+"&page=2", timeout = 10, headers=headers)
            content = BeautifulSoup(r.content, 'lxml')
            floors = content.find_all('div', id = re.compile("^post_[0-9]{8}"))
            for floor in floors:
                reply = floor.find('table').find('tr').find('td', class_='plc').find('table').get_text().strip().encode('utf-8').replace("rt", "").replace("\r\n", ", ").replace("\n", ", ").replace("\r", ", ").strip(", , ")
                tmp = reply.split(", ")
                if tmp[0].find(u'发表于') != -1:
                    reply = ", ".join(tmp[2:])
                threads.append(reply)
        return threads
    except Exception as e:
        return None


t0 = time.time()
currentTime = time.strftime("%Y-%m-%d-%H")
result = open("zuanke8." + str(currentTime) + ".txt", 'w')
qaResult = open("zuanke8." + str(currentTime) + ".qa.txt", 'w')
baseUrl = "http://www.zuanke8.com/forum.php?mod=forumdisplay&fid=15&orderby=dateline&orderby=dateline&filter=author"
for pageNum in xrange(1,50):
    pageNum = str(pageNum)
    content = getContent(baseUrl, pageNum)
    if content:
        ret = getPosts(content)
        for r in ret:
            result.write(";;".join(r) + "\n")
            idd = r[1]
            title = r[2].strip("...")
            threadUrl = r[3]
            threads = getThreads(threadUrl, title, idd)
            if threads:
                qaResult.write(";:;".join(threads)+ "\n")
            else: 
                print "error occur!!"
            time.sleep(0.1)
    time.sleep(0.5)