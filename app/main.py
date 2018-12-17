#!/usr/bin/python
# -*- coding: UTF-8 -*-

import robot
import thread
import time
import xml.sax
import socket               # 导入 socket 模块
from struct import *

# 为线程定义一个函数
def print_time(thread_name, delay):
    count = 0
    while True:
        time.sleep(delay)
        count += 1
        print "%s: %s" % (thread_name, time.ctime(time.time()))


print "Hello word!"

employee = robot.Employee("zhengruihui", 31)
employee.display_employee()

# 创建两个线程
try:
    thread.start_new_thread(print_time, ("Thread-1", 2,))
    thread.start_new_thread(print_time, ("Thread-2", 4,))
except:
    print "Error: unable to start thread"


class MovieHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.type = ""
        self.format = ""
        self.year = ""
        self.rating = ""
        self.stars = ""
        self.description = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "movie":
            print "*****Movie*****"
            title = attributes["title"]
            print "Title:", title

    # 元素结束事件处理
    def endElement(self, tag):
        if self.CurrentData == "type":
            print "Type:", self.type
        elif self.CurrentData == "format":
            print "Format:", self.format
        elif self.CurrentData == "year":
            print "Year:", self.year
        elif self.CurrentData == "rating":
            print "Rating:", self.rating
        elif self.CurrentData == "stars":
            print "Stars:", self.stars
        elif self.CurrentData == "description":
            print "Description:", self.description
        self.CurrentData = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "type":
            self.type = content
        elif self.CurrentData == "format":
            self.format = content
        elif self.CurrentData == "year":
            self.year = content
        elif self.CurrentData == "rating":
            self.rating = content
        elif self.CurrentData == "stars":
            self.stars = content
        elif self.CurrentData == "description":
            self.description = content


if (__name__ == "__main__"):


    # 重写 ContextHandler
    Handler = MovieHandler()

    parser = xml.sax.parse("movies.xml", Handler)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建 socket 对象
    host = "127.0.0.1"  # 获取本地主机名
    port = 12345
    s.bind((host, port))  # 绑定端口

    s_host = "127.0.0.1"
    s_port = 56789


    while True:
        s.sendto("hello", (s_host, s_port))

        data, addr = s.recvfrom(1024)  # 接收数据。
        print '连接地址：', data, addr

        s.sendto("hello", (s_host, s_port))
