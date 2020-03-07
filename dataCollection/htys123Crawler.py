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
    headers = {'User-Agent': ua, 'Referer': 'htys123.com', 'Connection': 'keep-alive', 'Host': 'www.htys123.com'}
    try:
        r = requests.get(url, timeout = 10, headers=headers)
        return BeautifulSoup(r.content, 'lxml')
    except Exception as e:
        if hasattr(e, "reason"):
            print "Failed:", e.reason
        return None   


def getPosts(content):
    currentTime = time.strftime("%Y-%m-%d-%H-%M")
    posts = content.find_all('th',class_='common')
    if len(posts) == 0:
        posts = content.find_all('th',class_='new')
    ret = []
    for post in posts:
        try:
            postId = post.find('a', class_='showcontent y').get("id").split("_")[1]
            href = post.find('a', class_='s xst')['href']
            title = post.find('a', class_='s xst').get_text().strip().encode('utf-8')
            ret.append([currentTime, postId, title, href])
        except:
            pass
    return ret
          

def getThreads(threadUrl, title, idd):
    s = requests.session()
    s.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 5
    ua = getUserAgent()
    headers = {'User-Agent': ua, 'Referer': 'htys123.com', 'Connection': 'keep-alive', 'Host': 'www.htys123.com'}
    threads = []
    try:
        r = requests.get(threadUrl, timeout = 10, headers=headers)
        content = BeautifulSoup(r.content, 'lxml')
        floors = content.find_all('div',class_='t_fsz')
        floors = content.find_all('td',class_='t_f')
        ret = []
        title2 = floors[0].get_text().strip().encode('utf-8').replace("\r\n", ", ").replace("\n", ", ").replace("\r", ", ")
        title2 = title2.strip(u'广告, , ,')
        if title2.startswith(title) and title2.decode('utf-8') >= title.decode('utf-8'):
            title = title2
        threads.append(idd)    
        threads.append(title)
        for floor in floors[1:]:
            reply = floor.get_text().strip().encode('utf-8').replace("\r\n", ", ").replace("\n", ", ").replace("\r", ", ")
            threads.append(reply)
        return threads
    except Exception as e:
        return None


result = open("/htysPosts.txt", 'a')
baseUrl = "http://www.htys123.com/forum.php?mod=forumdisplay&fid=2&filter=author&orderby=dateline"
for pageNum in xrange(1, 22):
    pageNum = str(pageNum)
    content = getContent(baseUrl, pageNum)
    if content:
        ret = getPosts(content)
        for r in ret:
            result.write(";;".join(r) + "\n")
    time.sleep(0.5)
    

questionAns = open("/htysPosts.qa.txt", "a")
for line in open("/htysPosts.txt" , 'r'):
    line = line.strip()
    try:
        parts = line.split(";;")
        idd = str(parts[1])
        title = parts[2].strip("...")
        threadUrl = parts[3]
        threads = getThreads(threadUrl, title, idd)
        if threads:
            questionAns.write(";:;".join(threads)+ "\n")
        time.sleep(0.3)
    except Exception as e:
        pass
