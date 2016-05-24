# coding: utf-8
# @desc Created by FavorTGD.
# @author : FavorMylikes<l786112323@gmail.com>
# @since : 2016/3/26 18:00
#用于验证IP端口是否开放
import socket
from queue import Queue
import threading
import time
import sys
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
class ExceptConter(dict):
    def add(self,type):
        if type in self:
            self[type]+=1
        else:
            self[type]=1
        self.print()
    def print(self):
        [print(c,end=' ') for c in self.items()]
class Ip_Port_authentic(threading.Thread):
    e_counter=ExceptConter()
    proxy_queue=Queue()
    log_file=None
    def authIpPort(self,ip,port):
        sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sk.settimeout(1)
        message=''
        try:
            sk.connect(('124.200.96.226',8188))
            message='<success:%s\t%s>' % (ip,port)
            self.e_counter.add('success')
            if self.log_file is not None:
                self.log_file.write('%s\t%s\n' % (ip,port))
                self.log_file.flush()
        except Exception as e:
            (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
            self.e_counter.add(ErrorType)
        print(message)
        sk.close()
    def run(self):
        while self.proxy_queue.qsize() !=0:
            (ip,port)=self.proxy_queue.get()
            port=port.replace("\n",'')
            self.authIpPort(ip,port)
if __name__ == '__main__':
    fileList=[
        r'F:\workspace_code\python\tool\IpProxyList1463725884.txt',
        r'F:\workspace_code\python\tool\IpProxyList1458929010.txt',
        r'F:\workspace_code\python\tool\IpProxyList1463331988.txt',
    ];
    ipProxylist=[]
    for file in fileList:
        ipProxylist+=getIpProxyList(file)
    ipProxylist=list(set(ipProxylist))
    [Ip_Port_authentic.proxy_queue.put((ip,port)) for (ip,port) in ipProxylist]
    timeStamp=int(time.time())
    Ip_Port_authentic.log_file=open('IpProxyEnableCouldConnectedList%d.txt' % timeStamp,'w')
    [Ip_Port_authentic().start() for i in range(40)]