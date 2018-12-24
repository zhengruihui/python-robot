#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
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


class MultiProcess(SocketManage):
    def __init__(self):
        SocketManage.__init__(self)
        pass


class RobotArm:
    def __init__(self):
        self.move_track = []


if __name__ == '__main__':

    # multi_process = MultiProcess()

    waypoint1 = [0, 1, 2, 3, 4, 5]

    waypoint2 = [0.1, 1.2, 2.1, 3.6, 4.009, 5.895]

    waypoint3 = [0.456, 1.2456, 2.4568, 3.3452, 4.367, 5.2577]

    move_track = [waypoint1, waypoint2, waypoint3]

    multiprocess = []

    multiprocess.append(move_track)
    multiprocess.append(move_track)

    for waypoint in multiprocess:
        print waypoint[1][0]

    # while True:
        # read_list = multi_process.get_read_list()
        # pass
