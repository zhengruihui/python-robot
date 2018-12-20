#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import xml.sax
import socket
from struct import *

import robotcontrol


ip_qt = "127.0.0.1"  # qt的ip与端口
port_qt = 01234

ip_python = "127.0.0.1"  # python的ip与端口
port_python = 56789

ip_aubot = "192.168.1.14"  # 机械手aubot的ip与端口
port_aubot = 8899


class QtData(threading.Thread):
    def __init__(self, read_ip="127.0.0.1", read_port=01234, write_ip="127.0.0.1", write_port=56789):
        threading.Thread.__init__(self)
        self.read_ip = read_ip
        self.read_port = read_port
        self.write_ip = write_ip
        self.write_port = write_port
        self.read_list = [0, 0, 0, 0, 0, 0]
        self.write_list = [0, 0, 0, 0.000]

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((read_ip, read_port))

    def run(self):
        while True:
            read_data, read_addr = self.s.recvfrom(1024)
            self.read_list = unpack('HHHHLf', read_data)
            print self.read_list[0]
            print self.read_list[1]
            print self.read_list[2]
            print self.read_list[3]
            print self.read_list[4]
            print self.read_list[5]


if __name__ == '__main__':
    # read_list = {0, 0, 0, 0, 0, 0.000}
    # data = "abcdefgabcdfaaaa"
    # read_list[0], read_list[1], read_list[2], read_list[3], read_list[4], read_list[5] = unpack('HHHHLf', data)

    qt_data = QtData()
    qt_data.start()
    qt_data.join()

