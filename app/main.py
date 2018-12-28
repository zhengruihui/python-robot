#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
import time
import xml.sax
import socket
from struct import *
# from robotcontrol import *
from xml.dom.minidom import parse
import xml.dom.minidom


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


class GetPlatform:
    def __init__(self):
        pass


class GetPlatformHandle:
    def __init__(self):
        pass


class PutPlatform:
    def __init__(self):
        pass


class PutPlatformHandle:
    def __init__(self):
        pass


class FDMPrint:
    def __init__(self):
        pass


class FDMPrintHandle:
    def __init__(self):
        pass

    def pdm_print(self):
        print "fdm_print"

class Start:
    def __init__(self):
        pass


class End:
    def __init__(self):
        pass


class Robot:
    def __init__(self):
        pass


class RobotHandle:
    def __init__(self):
        self.robot_thread = thread.allocate()
        # self.robot = robot_init()

    def move_joint(self, joint_list):
        self.robot_thread.acquire()
        print joint_list
        # logger.info("move joint to {0}".format(joint_radian))
        # self.robot.move_joint(oint_list[1:7])
        self.robot_thread.release()

    def get_platform(self):
        self.robot_thread.acquire()
        print "get_platform"
        self.robot_thread.release()

    def put_platform(self):
        self.robot_thread.acquire()
        print "put_platform"

        self.robot_thread.release()



class AssemblyLine:
    def __init__(self):
        pass


class MultiProcess:
    def __init__(self):
        pass


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
        child_list = assembly_line_xml.childNodes
        for child in child_list:    # level 0
            if child.nodeType == child.ELEMENT_NODE:
                if child.nodeName == "start":
                    start = Start()
                    start.name = child.nodeName
                    start.lock = child.getAttribute("lock")
                    assembly_line.process_list.append(start)

                if child.nodeName == "end":
                    end = End()
                    end.name = child.nodeName
                    end.lock = child.getAttribute("lock")
                    end.wait_type = child.getAttribute("wait_type")
                    assembly_line.process_list.append(end)

                if child.nodeName == "robot":
                    robot = Robot()
                    robot.name = child.nodeName
                    robot.joint_list = []
                    robot.joint_list.append(float(child.getAttribute("joint0")))
                    robot.joint_list.append(float(child.getAttribute("joint1")) / 57.2957805)
                    robot.joint_list.append(float(child.getAttribute("joint2")) / 57.2957805)
                    robot.joint_list.append(float(child.getAttribute("joint3")) / 57.2957805)
                    robot.joint_list.append(float(child.getAttribute("joint4")) / 57.2957805)
                    robot.joint_list.append(float(child.getAttribute("joint5")) / 57.2957805)
                    robot.joint_list.append(float(child.getAttribute("joint6")) / 57.2957805)

                    assembly_line.process_list.append(robot)

                if child.nodeName == "get_platform":
                    get_platform = GetPlatform()
                    get_platform.name = child.nodeName
                    assembly_line.process_list.append(get_platform)

                if child.nodeName == "put_latform":
                    put_latform = PutPlatform()
                    put_latform.name = child.nodeName
                    assembly_line.process_list.append(put_latform)

                if child.nodeName == "fdm_print":
                    fdm_print = FDMPrint()
                    fdm_print.name = child.nodeName
                    assembly_line.process_list.append(fdm_print)

    print "parse done"


class MultiProcessHandle:
    def __init__(self, multi_process):
        self.multi_process = multi_process
        self.thread_lock = thread.allocate()
        self.robot_handle = RobotHandle()
        self.fdm_print_handle = FDMPrintHandle()
        self.get_platform_handle = GetPlatformHandle()
        self.put_platform_handle = PutPlatformHandle()

        # 每条流水线一个线程
        for i in range(len(self.multi_process.assembly_line_list)):
            try:
                thread.start_new_thread(self.assembly_line_handle, (self.multi_process.assembly_line_list[i], ))
            except:
                print "Error: unable to start thread"

    def assembly_line_handle(self, assembly_line):
        while True:
            for i in range(assembly_line.times):
                process_list = assembly_line.process_list
                for process in process_list:

                    if process.name == "start":
                        print "start"
                        if process.lock == "true":
                            self.thread_lock.acquire()

                    if process.name == "end":
                        print "end"
                        if process.lock == "false":
                            self.thread_lock.release()
                        if process.wait_type == "fdm_print":
                            print "wait fdm_print"

                    if process.name == "robot":
                        self.robot_handle.move_joint(process.joint_list)

                    if process.name == "get_platform":
                        self.robot_handle.get_platform()

                    if process.name == "put_latform":
                        self.robot_handle.put_platform()

                    if process.name == "fdm_print":
                        self.fdm_print_handle.pdm_print()

                thread.exit_thread()


if __name__ == '__main__':

    multi_process = MultiProcess()
    parse_xml("process.xml", multi_process)
    multi_process_handle = MultiProcessHandle(multi_process)

    while True:
        pass


