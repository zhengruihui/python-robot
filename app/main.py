#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
import time
import xml.sax
import socket
from struct import *
from robotcontrol import *
from xml.dom.minidom import parse
import xml.dom.minidom


class Messages:
    def __init__(self, read_ip="127.0.0.1", read_port=01234, write_ip="127.0.0.1", write_port=56789):
        self.read_ip = read_ip
        self.read_port = read_port
        self.write_ip = write_ip
        self.write_port = write_port
        self.read_format = "c"
        self.write_format = "c"
        self.write_data = []

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((read_ip, read_port))

        # 创建线程
        try:
            thread.start_new_thread(self.read_thread, ())
        except:
            logger.error("Error: unable to start thread")

    def read_thread(self):
        while True:
            try:
                read_data, read_addr = self.s.recvfrom(1024)
                try:
                    read_list = unpack(self.read_format, read_data)
                    self.read(read_list)
                    del read_list
                except:
                    logger.error("unpack error!")
            except:
                logger.error("recvfrom error!")


    def read(self, read_list):
        pass

    def write(self, write_list):
        try:
            self.write_data = pack(self.write_format, *write_list)
            try:
                self.s.sendto(self.write_data, (self.write_ip, self.write_port))
            except:
                logger.error("sendto error!")
        except:
            logger.error("pack error!")


class CNC:
    def __init__(self):
        pass


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


class FDMPrintHandle(Messages):
    def __init__(self):
        Messages.__init__(self)
        self.read_lock = thread.allocate()
        self.write_lock = thread.allocate()
        self.read_format = "BBBB"
        self.write_format = "BBfffffffffffff"
        self.write_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.print_state_list = []

        # 创建线程
        try:
            thread.start_new_thread(self.write_thread, ())
        except:
            logger.error("Error: unable to start thread")

    def read(self, read_list):
        logger.debug(read_list)
        self.read_lock.acquire()
        if read_list[0] == 0:
            for i in range(len(self.print_state_list)):
                if read_list[1+i] == 1:
                    self.print_state_list[0+i] = True
                    logger.info("fdm %d done " % i)
                else:
                    self.print_state_list[0+i] = False

        if read_list[0] == 1:
            logger.info("start multi-process")
        if read_list[0] == 2:
            logger.info("end multi-process")
        self.read_lock.release()

    def finished(self, assembly_line_id):
        self.read_lock.acquire()
        state = self.print_state_list[assembly_line_id]
        self.read_lock.release()
        return state

    def pdm_print(self, assembly_line_id):
        self.write_lock.acquire()
        self.write_list[0] = 1
        self.write_list[1] = assembly_line_id
        self.write(self.write_list)
        self.print_state_list[assembly_line_id] = False
        self.write_lock.release()
        logger.info("fdm_print")

    def write_thread(self):
        while True:
            time.sleep(1)
            logger.debug("write_thread")
            self.write_lock.acquire()
            self.write_list[0] = 0
            self.write_list[1] = 0xff
            self.write_list[2] = 0.1
            self.write_list[3] = 0.2
            self.write_list[4] = 0.3
            self.write_list[5] = 0.4
            self.write_list[6] = 0.5
            self.write_list[7] = 0.6

            self.write_list[8] = 0.1
            self.write_list[9] = 0.2
            self.write_list[10] = 0.3

            self.write_list[11] = 0.1
            self.write_list[12] = 0.2
            self.write_list[13] = 0.3
            self.write_list[14] = 0.4
            self.write(self.write_list)
            self.write_lock.release()

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
        self.robot = robot_init()

    def move_joint(self, joint_list):
        self.robot_thread.acquire()
        self.robot.move_joint(joint_list[1:7])
        self.robot_thread.release()

    def get_platform(self):
        self.robot_thread.acquire()
        self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_02, 1)
        logger.info("get_platform")
        self.robot_thread.release()

    def put_platform(self):
        self.robot_thread.acquire()
        self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_02, 0)
        logger.info("put_platform")
        self.robot_thread.release()

    def open_cnc(self):
        self.robot_thread.acquire()
        self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_00, 1)
        logger.info("open_cnc")
        self.robot_thread.release()

    def close_cnc(self):
        self.robot_thread.acquire()
        logger.info("close_cnc")
        self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_00, 0)
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
        assembly_line.id = int(assembly_line_xml.getAttribute("id"))
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

                if child.nodeName == "cnc":
                    cnc = CNC()
                    cnc.name = child.nodeName
                    cnc.open = child.getAttribute("open")
                    assembly_line.process_list.append(cnc)

        logger.info("parse done")


class MultiProcessHandle:
    def __init__(self, multi_process):
        self.multi_process = multi_process
        self.thread_lock = thread.allocate()
        self.fdm_print_handle = FDMPrintHandle()
        self.get_platform_handle = GetPlatformHandle()
        self.put_platform_handle = PutPlatformHandle()
        self.robot_handle = RobotHandle()

        # 每条流水线一个线程
        for i in range(len(self.multi_process.assembly_line_list)):
            try:
                thread.start_new_thread(self.assembly_line_handle, (self.multi_process.assembly_line_list[i], ))
                self.fdm_print_handle.print_state_list.append(False)
            except:
                logger.debug("Error: unable to start thread")

    def assembly_line_handle(self, assembly_line):
        while True:
            for i in range(assembly_line.times):
                process_list = assembly_line.process_list
                for process in process_list:
                    if process.name == "start":
                        logger.debug("start")
                        if process.lock == "true":
                            self.thread_lock.acquire()

                    if process.name == "end":
                        logger.debug("end")
                        if process.lock == "false":
                            self.thread_lock.release()
                        if process.wait_type == "fdm_print":
                            logger.info("wait %d fdm_print" % assembly_line.id)
                            while not self.fdm_print_handle.finished(assembly_line.id):
                                pass

                    if process.name == "robot":
                        self.robot_handle.move_joint(process.joint_list)

                    if process.name == "get_platform":
                        self.robot_handle.get_platform()

                    if process.name == "put_latform":
                        self.robot_handle.put_platform()

                    if process.name == "fdm_print":
                        self.fdm_print_handle.pdm_print(assembly_line.id)

                    if process.name == "cnc":
                        if process.open == "true":
                            self.robot_handle.open_cnc()
                        if process.open == "false":
                            self.robot_handle.close_cnc()
            logger.info("assembly_line: %d have done" % assembly_line.id)
            thread.exit_thread()


if __name__ == '__main__':

    multi_process = MultiProcess()
    parse_xml("process.xml", multi_process)
    multi_process_handle = MultiProcessHandle(multi_process)

    while True:
        pass


