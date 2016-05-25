# coding: utf-8
# @desc Created by FavorTGD.
# @author : FavorMylikes<l786112323@gmail.com>
# @since : 2016/3/24 15:25
import gzip
import json
import re
import sys
import time
import urllib.request
import urllib.parse
import os
from queue import Queue
import threading
import socket

from lxml import etree
import execjs
# from plant_spider.lxml import etree
# from  plant_spider import execjs
from urllib.error import URLError,HTTPError
urls=[
    # 'http://www.baidu.com',
    # 'http://bhysnack.science/mylikes/,'#测试高匿代理
    'http://blog.tingyun.com/web/article/detail/587',
    'http://www.thinkphp.cn/topic/39141.html',
    'https://yq.aliyun.com/articles/43809',
    'http://www.ituring.com.cn/article/215536',
    'http://www.tuicool.com/articles/a2iyyq6',
    'http://toutiao.com/i6285476344562188802/',
    'http://www.shaoqun.com/a/221198.aspx',
    'http://www.cnblogs.com/TingyunAPM/p/5489855.html',
]
# url='https://www.baidu.com/'
# url='http://www.stilllistener.com/checkpoint1/test2/'

headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    # "Host":"blog.tingyun.com",
    # "Referer":"http://blog.tingyun.com/web/article/list/catalog/1?page=1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
    "Cache-Control":"max-age=0",}
def getIpProxyList(file='IpProxyList.txt'):
    result=[]
    for line in open(file,'r'):
        try:
            datas=line.split('\t')
            ip=line.split('\t')[0]
            port=line.split('\t')[1]
            if len(datas)==3 and int(datas[2])!=3:
                continue
        except Exception as e:
            print(e.__class__)
        result.append((ip,port))
    return result
class ConnectionRefusedError_10061(ConnectionRefusedError):
    pass
class ConnectionRefusedError_10054(ConnectionRefusedError):
    pass
class spider(threading.Thread):
    proxy_queue=Queue()
    lock=threading.Lock()
    lock_proxy=threading.Lock()
    log_file=None
    counter={}
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while self.proxy_queue.qsize() !=0:
            (ip,port)=self.proxy_queue.get()
            port=port.replace("\n",'')
            # proxy={'http':'http://%s:%s/' % (ip,port)}
            # porxy_support=urllib.request.ProxyHandler(proxy)
            # opener=urllib.request.build_opener(porxy_support)
            # urllib.request.install_opener(opener)
            for url in urls:
                req=urllib.request.Request(url,headers=headers)
                req.method='GET'
                req.set_proxy('%s:%s' % (ip,port),type='http')
                try:
                    err_count=0
                    errlimit=4
                    while err_count<errlimit:
                        try:
                            byte=urllib.request.urlopen(req,timeout=6)
                            page=byte.read()
                            break
                        except socket.timeout as e:
                            err_count+=1
                            if err_count>=errlimit:
                                raise e
                        except urllib.error.HTTPError as e:
                            err_count+=1
                            if err_count>=errlimit:
                                raise e
                        except urllib.error.URLError as e:
                            value=e.args[0]
                            if isinstance(value,ConnectionRefusedError):
                                err_count+=1
                                if value.args[0]==10061:
                                    raise ConnectionRefusedError_10061(value.args)
                                elif value.args[0]==10054:
                                    raise ConnectionRefusedError_10054(value.args)
                                else:
                                    raise value
                            elif isinstance(e.args[0],socket.timeout):
                                err_count+=1
                                if err_count>=errlimit:
                                    raise value
                            else:
                                raise value
                        except Exception as e:
                            err_count+=1
                            if err_count>=errlimit:
                                raise e
                    #################验证代理匿名程度
                    # try:
                    #     data=gzip.decompress(page).decode('utf8','ignore')
                    # except:
                    #     data=page.decode('gbk','ignore')
                    # tree=etree.HTML(data)
                    # anony_level=tree.xpath('//*[@id="level"]')[0].text
                    # if self.log_file is not None:
                    #     self.log_file.write('%s\t%s\t%s\n' % (ip,port,anony_level))
                    #     self.log_file.flush()
                    ################结束验证
                    self.lock.acquire()
                    if 'success' in self.counter:
                        self.counter['success']+=1
                    else:
                        self.counter['success']=1
                    self.lock.release()
                    # if self.counter['success']>1000:
                    #     break
                    message=''
                except Exception as e:
                    self.lock.acquire()
                    if e.__class__ in self.counter:
                        self.counter[e.__class__]+=1
                    else:
                        self.counter[e.__class__]=1
                    self.lock.release()
                    message=e.args
                [print(c,end=' ') for c in self.counter.items()]
                print(message)
                sys.stdout.flush()

if __name__=='__main__':
    fileList=[
        r'F:\workspace_code\python\tool\IpProxyList1463725884.txt',
        r'F:\workspace_code\python\tool\IpProxyList1458929010.txt',
        r'F:\workspace_code\python\tool\IpProxyList1463331988.txt',
    ];
    ipProxylist=[]
    for file in fileList:
        ipProxylist+=getIpProxyList(file)
    ipProxylist=list(set(ipProxylist))
    [spider.proxy_queue.put((ip,port)) for (ip,port) in ipProxylist]
    spider.log_file=open('IpProxyEnableList1463725885.txt','w')
    # spider.proxy_queue.put(("183.207.228.44","80"))
    [spider().start() for i in range(40)]