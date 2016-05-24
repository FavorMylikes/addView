# coding: utf-8
# @desc Created by FavorTGD.
# @author : FavorMylikes<l786112323@gmail.com>
# @since : 2016/3/24 17:05
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
from lxml import etree
import execjs
from urllib.error import URLError,HTTPError

def _print(args, sep=' ', end='\n', file=None,out=sys.stdout):
    old=sys.stdout
    sys.stdout=out
    print(time.strftime("%Y-%m-%d %H:%M:%S"),end='\t')
    print(args,sep)
    sys.stdout=old
class main():

    headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip,deflate,sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        "Host":"www.kuaidaili.com",
        # "Cache-Control":"max-age=0",
        "Connection":"keep-alive"}
    root_url='http://www.kuaidaili.com/free/inha/%d/'
    def __init__(self):
        self.log_err=open('error%s.txt' % time.strftime("%Y%m%d%H%M%S"),'w')
    def urlopen_with_except(self,req):
        i=0
        while True:
            i+=1
            if i>5:
                _print(req._full_url+"  Can not connected this url")
                break
            try:
                byte=urllib.request.urlopen(req,timeout=4)
                page=byte.read()
                return page
            except HTTPError as e:
                _print(req._full_url+' Error code:',e.code,out=self.log_err)
            except URLError as e:
                _print(req._full_url+' Reason:',e.reason,out=self.log_err)
            except Exception as e:
                _print(req._full_url+' Exception',e.__class__,out=self.log_err)
    def spider(self,url):
        req=urllib.request.Request(url,headers=self.headers)
        page=self.urlopen_with_except(req)
        if page is None:
            return None
        try:
            data=gzip.decompress(page).decode('gbk','ignore')
        except Exception as e:
            data=page.decode('gbk','ignore')
        return data
    def get_ip_port(self,data):
        results=[]
        tree=etree.HTML(data)
        # items=tree.xpath('//*[@id="ip_list"]/tr')
        items=tree.xpath('//tr')
        for i in range(len(items)-1):

            try:
                ip=tree.xpath('//*[@id="list"]/table/tbody/tr[%d]/td[1]' % (int(i)+1))[0].text
                port=tree.xpath('//*[@id="list"]/table/tbody/tr[%d]/td[2]' % (int(i)+1))[0].text
                # ip=tree.xpath('//*[@id="ip_list"]/tr[%d]/td[3]' % (int(i)+2))[0].text
                # port=tree.xpath('//*[@id="ip_list"]/tr[%d]/td[4]' % (int(i)+2))[0].text
            except:
                pass
            results.append((ip,port))
        return results
if __name__=='__main__':
    old=sys.stdout
    sys.stdout=open('IpProxyList%d.txt' % int(time.time()),'w')
    m=main()
    i=1
    for pager in range(1,1051):
        data=m.spider('http://www.kuaidaili.com/free/inha/%d/' % pager)
        if data is None:
            continue
        items=m.get_ip_port(data)
        for (ip,port) in items:
            print(ip+"\t"+port)
            if i%10==0:
                _print(i,out=old)
            i+=1
    # for pager in range(1,717):
    #     data=m.spider('http://www.xicidaili.com/nn/%d' % pager)
    #     if data is None:
    #         continue
    #     items=m.get_ip_port(data)
    #     for (ip,port) in items:
    #         print(ip+"\t"+port)
    #         if i%10==0:
    #             _print(i,out=old)
    #         i+=1
    sys.stdout=old