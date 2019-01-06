#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket
import thread
from struct import *
COMMAND = 0
READ = 0
WRITE = 1
START = 2

UPLOAD = 1
DOWNLOAD = 2
FDMSTATE = 3


def memory_share_set(memory_list, index_x, index_y, data):
    index_x_list = memory_list[index_x]
    index_x_list[index_y] = data
    memory_list[index_x] = index_x_list


class Protocol:
    def __init__(self, memory_share):
        self.read_ip = "127.0.0.1"
        self.read_port = 12345
        self.write_ip = "127.0.0.1"
        self.write_port = 56789
        self.memory_share = memory_share

        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.bind((self.read_ip, self.read_port))
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 创建线程

        thread.start_new_thread(self.read, ())
        thread.start_new_thread(self.write, ())

    def read(self):
        while True:
            read_data = self.recv_socket.recv(1024)
            read_list = unpack("BBBB", read_data)
            self.memory_share[DOWNLOAD] = read_list
            memory_share_set(self.memory_share, COMMAND, READ, "set")
            pass

    def write(self):
        while True:
            if self.memory_share[COMMAND][WRITE] == "set":
                memory_share_set(self.memory_share, COMMAND, WRITE, "clear")
                write_list = self.memory_share[UPLOAD]
                write_data = pack("BBfffffffffffff", *write_list)
                self.send_socket.sendto(write_data, (self.write_ip, self.write_port))


