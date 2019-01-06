#!/usr/bin/python
# -*- coding: UTF-8 -*-
import multiprocessing
import time
from parse_xml import *
from robotcontrol import *
from protocol import *


class FDMPrintHandle:
    def __init__(self):
        self.print_state_list = []

    def finished(self, assembly_line_id):
        state = self.print_state_list[assembly_line_id]
        return state

    def start_print(self, assembly_line_id):
        logger.info("start_print: %d" % assembly_line_id)


class RobotHandle(multiprocessing.Process):
    def __init__(self, read_queue, write_queue):
        multiprocessing.Process.__init__(self)
        self.robot = robot_init()
        self.read_queue = read_queue
        self.write_queue = write_queue

    def move_joint(self, joint_list):
        # self.robot.move_joint(joint_list[1:7])
        print joint_list

    def get_platform(self):
        # self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_02, 1)
        logger.info("get_platform")

    def put_platform(self):
        # self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_02, 0)
        logger.info("put_platform")

    def open_cnc(self):
        # self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_00, 1)
        print "open_cnc"

    def close_cnc(self):
        # self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_00, 0)
        print "close_cnc"

    def run(self):
        while True:
            if not self.read_queue.empty():
                read_data = self.read_queue.get(False)
                if read_data[0] == "joint":
                    self.move_joint(read_data[1:7])
                    data_list = ["done"]
                    if not self.write_queue.full():
                        self.write_queue.put_nowait(data_list)

                if read_data[0] == "open_cnc":
                    self.open_cnc()

                if read_data[0] == "close_cnc":
                    self.close_cnc()


def assembly_line_handle(assembly_line, read_queue, write_queue, memory_share):
    print_state = 0
    while True:
        if memory_share[COMMAND][START] == "set":
            memory_share_set(memory_share, COMMAND, START, "clear")
            print_state = 1

        if print_state == 0:
            pass

        if print_state == 1:
            print "assembly_line: %d start" % assembly_line.id
            for count in range(assembly_line.times):
                process_list = assembly_line.process_list
                for process in process_list:
                    if process.name == "start":
                        if process.lock == "true":
                            # self.thread_lock.acquire()
                            pass

                    if process.name == "end":
                        # logger.debug("end")
                        if process.lock == "false":
                            # self.thread_lock.release()
                            pass
                        if process.wait_type == "fdm_print":
                            pass

                    if process.name == "robot":
                        if not write_queue.full():
                            write_queue.put_nowait(process.joint_list)
                            while True:
                                if not read_queue.empty():
                                    read_data = read_queue.get(False)
                                    if read_data[0] == "done":
                                        print "done"
                                        break


                        # self.robot_handle.move_joint(process.joint_list)
                        pass
                    if process.name == "get_platform":
                        # self.robot_handle.get_platform()
                        pass
                    if process.name == "put_latform":
                        # self.robot_handle.put_platform()
                        pass
                    if process.name == "fdm_print":
                        memory_share_set(memory_share, UPLOAD, 0, 1)
                        memory_share_set(memory_share, UPLOAD, 1, assembly_line.id)
                        memory_share_set(memory_share, COMMAND, WRITE, "set")
                        pass
                    if process.name == "cnc":
                        if process.open == "true":
                            data_list = ["open_cnc"]
                            if not write_queue.full():
                                write_queue.put_nowait(data_list)
                            # self.robot_handle.open_cnc()
                            pass
                        if process.open == "false":
                            # self.robot_handle.close_cnc()
                            data_list = ["close_cnc", assembly_line.id]
                            if not write_queue.full():
                                write_queue.put_nowait(data_list)
                            pass
            print_state = 0
            print "assembly_line: %d done" % assembly_line.id


def protocol_f(memory_share):
    protocol = Protocol(memory_share)
    while True:
        pass


if __name__ == '__main__':
    multi_process = parse_xml("process.xml")
    queue_read_list = []
    queue_write_list = []
    processing_list = []

    command = [0, 0, 0, 0]
    upload = [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    download = [0, 0, 0, 0]
    fdm_state = []

    read_queue = multiprocessing.Queue()
    write_queue = multiprocessing.Queue()
    read_queue_p = multiprocessing.Queue()
    write_queue_p = multiprocessing.Queue()
    manager = multiprocessing.Manager()
    memory_share = manager.list()
    memory_share.append(command)
    memory_share.append(upload)
    memory_share.append(download)
    memory_share.append(fdm_state)

    processing = RobotHandle(write_queue, read_queue)
    processing.start()

    processing = multiprocessing.Process(target=protocol_f, args=(memory_share, ))
    processing.start()

    for assembly_linex in multi_process.assembly_line_list:
        processing = multiprocessing.Process(target=assembly_line_handle, args=(assembly_linex, read_queue, write_queue, memory_share))
        processing_list.append(processing)
        fdm_state.append(0)
    for processing in processing_list:
        processing.start()
    while True:
        if memory_share[COMMAND][READ] == "set":
            memory_share_set(memory_share, COMMAND, READ, "clear")
            if memory_share[DOWNLOAD][0] == 1:
                memory_share_set(memory_share, COMMAND, START, "set")
            if memory_share[DOWNLOAD][0] == 0:
                memory_share[FDMSTATE] = memory_share[DOWNLOAD][1:len(memory_share[FDMSTATE])]

        pass
