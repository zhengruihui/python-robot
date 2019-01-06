#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
import time

from struct import *
from robotcontrol import *
from parse_xml import *
from protocol import *
import multiprocessing


class FDMPrintHandle:
    def __init__(self):
        self.print_state_list = []

    def finished(self, assembly_line_id):
        state = self.print_state_list[assembly_line_id]
        return state

    def start_print(self, assembly_line_id):
        logger.info("start_print: %d" % assembly_line_id)


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


class MultiProcessHandle:
    def __init__(self, multi_p):
        self.multi_process = multi_p
        self.thread_lock = thread.allocate()
        self.fdm_print_handle = FDMPrintHandle()
        self.robot_handle = RobotHandle()

        # 每条流水线一个线程
        for i in range(len(self.multi_process.assembly_line_list)):
            thread.start_new_thread(self.assembly_line_handle, (self.multi_process.assembly_line_list[i], ))
            self.fdm_print_handle.print_state_list.append(False)

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
                        self.fdm_print_handle.start_print(assembly_line.id)

                    if process.name == "cnc":
                        if process.open == "true":
                            self.robot_handle.open_cnc()
                        if process.open == "false":
                            self.robot_handle.close_cnc()
            logger.info("assembly_line: %d have done" % assembly_line.id)
            thread.exit_thread()


def protocol_f(read_queue, write_queue):
    protocol = Protocol(read_queue, write_queue)
    while True:
        pass


def multi_process_f(read_queue, write_queue):
    # multi_process = MultiProcess()
    # parse_xml("process.xml", multi_process)
    # multi_process_handle = MultiProcessHandle(multi_process)

    while True:
        if not read_queue.empty():
            read_data = read_queue.get(False)
            print "received: %s" % read_data
            if not write_queue.full():
                write_queue.put(read_data, False)


if __name__ == '__main__':

    queue_w = multiprocessing.Queue()
    queue_r = multiprocessing.Queue()

    processing_protocol = multiprocessing.Process(target=protocol_f, args=(queue_r, queue_w))
    processing_assembly = multiprocessing.Process(target=multi_process_f, args=(queue_w, queue_r))

    processing_protocol.start()
    processing_assembly.start()

    processing_protocol.join()
    processing_assembly.join()





