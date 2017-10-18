#coding:utf-8
import urllib.request 
import requests
import threading
import re
import random
import queue
import os
from bs4 import BeautifulSoup
import codecs
import time
import sys

time_begin = time.time()
mutex = threading.Lock()
ThreadsNum = 10
ImgNum = 1000000000
ThirdImgUrlNum = 0
ImgPer = ImgNum
argvs = sys.argv
ImgSavedPath = sys.path[0].replace("\\","/") + "/pics"
imgUrls = queue.Queue()
SecondimgUrls_First = queue.Queue()
SecondimgUrls = queue.Queue()
ThirdImgUrls = queue.Queue()
HomeUrl = "http://www.juemei.com"
RegHref = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
RegSrc = r"(?<=src=\").+?(?=\")|(?<=src=\').+?(?=\')"
proxies = queue.Queue()
#应付反爬虫，设置代理IP
Header = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
            'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
            'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
            ]
Webheader= [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'},
            {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'}
            ]
Webheader2= [
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1')],
            [('User-Agent', 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1')],
            [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3')],
            [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24')],
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24')]
            ]
#python test.py -l 10
def getUrlBeforeProxy(url,tagName, Attrs, reg):
    '''
    req = urllib.request.Request(url=url,headers={'User-Agent':random.choice(Header)})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    '''
    html = requests.get(url,headers=random.choice(Webheader)).text
    soup = BeautifulSoup(html,"html.parser") 
    content = str(soup.find_all(name = tagName, attrs = Attrs))
    return re.findall(reg ,content)
def getUrl(url,tagName, Attrs, reg):
    try:
        html = requests.get(url,headers=random.choice(Webheader)).text
        print("链接获取成功",url)
        soup = BeautifulSoup(html,"html.parser") 
        content = str(soup.find_all(name = tagName, attrs = Attrs))
        return re.findall(reg ,content) 

    except Exception as e:
        print("链接获取失败，正在重新获取","failed!")
        print(e)
    
def get_proxy():
    IPS = queue.Queue()
    PORTS = queue.Queue()
    global proxies
    print("开始获取代理IP")
    for e in getUrlBeforeProxy("http://www.xicidaili.com","tr",{"class":"odd"},r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'):
        IPS.put(e)
    for e in getUrlBeforeProxy("http://www.xicidaili.com","tr",{"class":"odd"},r'<td>\d{2,5}</td>'):
        PORTS.put(e[4:e.index("</")])
    print("获取到",PORTS.qsize(),"个代理IP")
    proxiesNum = 0
    while proxiesNum < 5 and not IPS.empty() and not PORTS.empty():
        proxy = IPS.get() + ":" + PORTS.get()
        try:
            print("xxx",proxy)
            html = requests.get("http://www.baidu.com",headers=random.choice(Webheader),proxies={'http':proxy},timeout=2)
            proxies.put(proxy)
            proxiesNum += 1
            print(proxy,"Success!!","%d/5" % proxiesNum)
        except Exception as e:
            print(proxy,"failed!","%d/5" % proxiesNum)
            print(e)
            continue
    print(proxiesNum,"个代理准备好了")
    
def makeSecondImgUrlsWorker(url,ThreadID):
    maxPage = max(int(x) for x in getUrl(url, "div",{"class":"page"}, r"\d+?\d*"))
    for i in range(2,maxPage + 1):
        #/mm/l.html特殊处理
        if url.count("html") == 1:
            SecondimgUrls.put(url[:url.index(".html")] + "_" + str(i) + ".html")
        else:
        #形如/mm/meitui/
            SecondimgUrls.put(url + "index_" + str(i) + ".html")        
            
class makeSecondImgUrls(threading.Thread):
    def __init__(self,ThreadID):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
    
    def run(self):
        print("构造SecondUrls线程",self.ThreadID,"开始......")
        while True:
            if not SecondimgUrls_First.empty():
                Url = SecondimgUrls_First.get()
                makeSecondImgUrlsWorker(Url,self.ThreadID)
                SecondimgUrls_First.task_done
            else:
                break
        print("构造SecondUrls线程",self.ThreadID,"完成")
                
def getThirdImgUrlsWorker(Url,ThreadID):
    global ThirdImgUrlNum
    for url in getUrl(Url, "div", {"class":"waterfall"}, RegHref):
        #需要控制进入队列的个数，加锁
        with mutex:
            if ThirdImgUrlNum > 0:
                ThirdImgUrls.put(HomeUrl + url)
                print("获取ThirdUrls",HomeUrl + url,ThreadID,ThirdImgUrlNum)
                ThirdImgUrlNum -= 1

class getThirdImgUrls(threading.Thread):
    def __init__(self, ThreadID):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
    def run(self):
        global ThirdImgUrlNum
        while ThirdImgUrlNum > 0:
            if(not SecondimgUrls.empty()):
                Url = SecondimgUrls.get()
                getThirdImgUrlsWorker(Url,self.ThreadID)
                SecondimgUrls.task_done
            else:
                break
        
def getImgUrlsWorker(imgHtmlUrl,ThreadID):
    global ImgNum
    for url in getUrl(imgHtmlUrl, "div", {"class":"album_wrap"}, RegSrc):
        #需要控制进入队列的个数，加锁
        with mutex:
            if 0 < ImgNum:
                imgUrls.put(url)
                ImgNum -= 1
            
class getImgUrls(threading.Thread):
    def __init__(self, ThreadID):
        self.content = ""
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
        
    def run(self):
        print("获取imgUrl线程",self.ThreadID,"开始......")
        while True:
            if(not ThirdImgUrls.empty()):
                imgUrl = ThirdImgUrls.get()
                getImgUrlsWorker(imgUrl,self.ThreadID)
                ThirdImgUrls.task_done
            else:
                break
        print("获取imgUrl线程",self.ThreadID,"结束")

class getImg(threading.Thread):
    def __init__(self,ThreadID):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
    def run(self):
        print("下载线程",self.ThreadID,"开始......")
        while not imgUrls.empty():
            url = imgUrls.get().replace("_s.",".")   
            proxy = {'http':proxies.get()}
            res = requests.get(url,headers=random.choice(Webheader),proxies=proxy)
            proxies.put(proxy)
            filename=ImgSavedPath + "/" + url[url.index(".com")+5:].replace("/","_")
            with open(filename,'wb') as f:
                print(proxy,url, "Downloading...... Done",self.ThreadID)
                f.write(res.content)
        print("下载线程",self.ThreadID,"结束")

def Distinct(Q):
    a = Q.qsize()
    print("开始个数",a)
    s = set()
    while not Q.empty():
        s.add(Q.get())
    print("集合大小",len(s))
    for item in s:
        Q.put(item)
    print("结束个数",Q.qsize())
    return [a - Q.qsize(),Q]
    print("结束去重")

def getThirdUrl():
    threads = []
    for i in range(ThreadsNum):
        t = getThirdImgUrls(i)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
def getImgUrl():
    threads = []
    for i in range(ThreadsNum):
        t = getImgUrls(i) 
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    
def plusMakeThirdImgUrls():
    while not ThirdImgUrls.empty():
        ThirdImgUrls.get()
    #从http://www.juemei.com/mm/meitui/index_5.html开始
    for i in range(ThirdImgUrlNum):
        SecondimgUrls.put("http://www.juemei.com/mm/meitui/index_" + str(5 - i) + ".html")
    getThirdUrl()
    
    
if __name__=="__main__":
    get_proxy()
    threads = []
    if "-h" in argvs:
        print("Help:")
        print("-n: Assign the number of concurrent threads")
        print("    Default: 10 ")
        print("    Example: python mm_crawler.py -n 20")
        
        print("-o: Assign the absolute path of images where they'd be saved")
        print("    Default: " + ImgSavedPath)
        print("    Example: python mm_crawler.py -o 'D:/pics'")
        
        print("-l: Assign the maximum number of images")
        print("    Default: no restriction ")
        print("    Example: python mm_crawler.py -l 2000")
    else:
        if "-n" in argvs:
            ThreadsNum = int(argvs[argvs.index("-n") + 1])
        if "-o" in argvs:
            ImgSavedPath = argvs[argvs.index("-o") + 1]
            
        if "-l" in argvs:
            ImgNum = int(argvs[argvs.index("-l") + 1])
            ImgPer = ImgNum
        
        print("ThreadsNum:",ThreadsNum,"path:",ImgSavedPath,"ImgNum:",ImgNum)
        if not os.path.exists(ImgSavedPath):
        
            os.mkdir(ImgSavedPath)
            
        print("开始获取链接")
        #获取部分ThirdImgUrls和全部SecondimgUrls_First
        ThirdImgUrlNum = ImgNum//5
        for url in getUrl(HomeUrl+"/mm","div",{"class":"focus wrapper"},RegHref):
            #形如：http://www.juemei.com/mm/201609/5420.html，含多个imgUrls
            if ThirdImgUrlNum > 0:
                ThirdImgUrls.put(HomeUrl + url)
                ThirdImgUrlNum -= 1
        
        for url in getUrl(HomeUrl+"/mm",'div', {"class":"rec_list wrapper cf"},RegHref):
            if url.count("/") == 3:
                #形如/mm/201609/5420.html，含多个imgUrls
                if ThirdImgUrlNum > 0:
                    if ThirdImgUrlNum > 0:
                        ThirdImgUrls.put(HomeUrl + url)
                        ThirdImgUrlNum -= 1
            else:
                #/mm/1.html 特殊处理,包含多个SecondimgUrls
                SecondimgUrls_First.put(HomeUrl + url)
        for url in getUrl(HomeUrl+"/mm",'div', {"class":"category_main"},RegHref):
            #形如：http://www.juemei.com/mm/meitui/，包含多个ThirdImgUrls
            SecondimgUrls_First.put(HomeUrl + url)
            print(HomeUrl + url)
        #构造SecondimgUrls
        for i in range(ThreadsNum):
            t = makeSecondImgUrls(i)
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        
        #获取ThirdUrls 
        getThirdUrl()
        
        print("ThirdImgUrls开始去重......")
        tmp = Distinct(ThirdImgUrls)
        ThirdImgUrls = tmp[1]
        print("去掉",tmp[0],"个重复的ThirdImgUrl")
        
        #获取每张图片的Url
        getImgUrl()        
        
        print("imgUrls开始去重......")
        tmp = Distinct(imgUrls)
        ImgNum = tmp[0]
        imgUrls = tmp[1]
        print("去掉",ImgNum,"个重复的imgUrls")
        idx = 1
        
        #循环添加、去重，直到没有重复出现
        while ImgNum > 0 and idx < 6:
            print("第",idx,"次循环去重imgUrls")
            ThirdImgUrlNum = max(ImgNum//120,1)
            plusMakeThirdImgUrls()
            getImgUrl()
            tmp = Distinct(imgUrls)
            ImgNum = tmp[0]
            print("去掉",ImgNum,"个重复的imgUrls")
            imgUrls = tmp[1]
            #避免死循环,避免第二次循环下载相同图片
            idx += 1
        
        '''
        print("链接获取完成")
        tmp = imgUrls
        with codecs.open("D:/mm_crawler/imgUrls.txt","w","utf-8") as fw:
            while not tmp.empty():
                fw.write(tmp.get() + "\n")
        print(imgUrls.qsize())
        '''
        
        time.sleep(3)
        print("开始下载图片")
        threads = []
        for i in range(ThreadsNum):
            t = getImg(i) 
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        print("图片下载完成")
        