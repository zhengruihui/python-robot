#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
import time
import xml.sax
import socket
from struct import *

from xml.dom.minidom import parse
import xml.dom.minidom

import robotcontrol


ip_qt = "127.0.0.1"  # qt的ip与端口
port_qt = 01234

ip_python = "127.0.0.1"  # python的ip与端口
port_python = 56789

ip_aubot = "192.168.1.14"  # 机械手aubot的ip与端口
port_aubot = 8899


class SocketManage:
    def __init__(self, read_ip="127.0.0.1", read_port=01234, write_ip="127.0.0.1", write_port=56789):
        self.read_ip = read_ip
        self.read_port = read_port
        self.write_ip = write_ip
        self.write_port = write_port
        self.read_list = [0]
        self.write_list = [0]

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((read_ip, read_port))
        self.read_lock = thread.allocate()
        self.write_lock = thread.allocate()

        # 创建两个线程
        try:
            thread.start_new_thread(self.read_thread, ())
            thread.start_new_thread(self.write_thread, ())

        except:
            print "Error: unable to start thread"

    def read_thread(self):
        while True:
            read_data, read_addr = self.s.recvfrom(1024)
            self.read_lock.acquire()
            self.read_list = unpack('HHHHLf', read_data)
            self.read_lock.release()

    def write_thread(self):
        while True:
            self.write_lock.acquire()
            time.sleep(1)
            print "write_thread"
            self.write_lock.release()

    def get_read_list(self):
        self.read_lock.acquire()
        read_list = self.read_list
        self.read_lock.release()
        return read_list

    def set_write_list(self, write_list):
        self.write_lock.acquire()
        self.write_list = write_list
        self.write_lock.release()


class Get:
    def __init__(self):
        pass


class Put:
    def __init__(self):
        pass


class Start:
    def __init__(self):
        pass


class Coordidate:
    def __init__(self):
        pass


class Process:
    def __init__(self):
        pass


class AssemblyLine:
    def __init__(self):
        pass


class MultiProcess:
    def __init__(self):
        pass


class MultiProcessHandle:
    def __init__(self, multi_process):
        self.multi_process = multi_process

        # 每条流水线一个线程
        for i in range(len(multi_process.assembly_line_list)):
            try:
                thread.start_new_thread(self.assembly_line_handle, (multi_process.assembly_line_list[i], ))
            except:
                print "Error: unable to start thread"

    def assembly_line_handle(self, assembly_line):
        while True:
            for i in range(assembly_line.times):
                print assembly_line.id
                for process in assembly_line.process_list:
                    print process.name

            thread.exit_thread()


def parse_xml(xml_name, multi_process):
    # 使用minidom解析器打开 XML 文档
    dom_tree = xml.dom.minidom.parse(xml_name)
    multi_process_xml = dom_tree.documentElement
    multi_process.assembly_line_list = []
    multi_process.name = multi_process_xml.getAttribute("name")
    assembly_line_xml_list = multi_process_xml.getElementsByTagName("assembly_line")
    for assembly_line_xml in assembly_line_xml_list:
        assembly_line = AssemblyLine()
        assembly_line.process_list = []
        assembly_line.id = assembly_line_xml.getAttribute("id")
        assembly_line.times = int(assembly_line_xml.getAttribute("times"))
        multi_process.assembly_line_list.append(assembly_line)
        child_0_list = assembly_line_xml.childNodes
        for child_0 in child_0_list:    # level 0
            if child_0.nodeType == child_0.ELEMENT_NODE:
                if child_0.nodeName == "process":
                    process = Process()
                    process.list = []
                    process.name = child_0.getAttribute("name")
                    assembly_line.process_list.append(process)
                    child_1_list = child_0.childNodes
                    for child_1 in child_1_list:    # level 1
                        if child_1.nodeType == child_1.ELEMENT_NODE:
                            if child_1.nodeName == "coordidate":
                                coordidate = Coordidate()
                                coordidate.name = child_1.nodeName
                                coordidate.joint0 = float(child_1.getAttribute("joint0"))
                                coordidate.joint1 = float(child_1.getAttribute("joint1"))
                                coordidate.joint2 = float(child_1.getAttribute("joint2"))
                                coordidate.joint3 = float(child_1.getAttribute("joint3"))
                                coordidate.joint4 = float(child_1.getAttribute("joint4"))
                                coordidate.joint5 = float(child_1.getAttribute("joint5"))
                                coordidate.joint6 = float(child_1.getAttribute("joint6"))
                                process.list.append(coordidate)

                            if child_1.nodeName == "get":
                                get = Get()
                                get.name = child_1.nodeName
                                process.list.append(get)

                            if child_1.nodeName == "put":
                                put = Put()
                                put.name = child_1.nodeName
                                process.list.append(put)

                            if child_1.nodeName == "start":
                                start = Start()
                                start.name = child_1.nodeName
                                process.list.append(start)
    print "parse done"

if __name__ == '__main__':

    multi_process = MultiProcess()
    parse_xml("process.xml", multi_process)
    multi_process_handle = MultiProcessHandle(multi_process)

    while True:
        pass


