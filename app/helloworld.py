#!/usr/bin/python
# -*- coding: UTF-8 -*-

from multiprocessing import  Process,Manager,Value,Array
import socket
from struct import *
import time
import thread
from parse_xml import *
from robotcontrol import *
import thread

STANDBY = 0
MOTION_MOVE = 1
ROBOT_MOVE = 2

SET = 1
CLEAR = 0
INDEX_RECV_FLAG = 0
INDEX_SEND_FLAG = 1
INDEX_JOINT_FLAG = 2
INDEX_CNC_OPEN_FLAG = 3
INDEX_CNC_CLOSE_FLAG = 4
INDEX_CLAW_OPEN_FLAG = 5
INDEX_CLAW_CLOSE_FLAG =6
INDEX_FDM_FLAG = 7
INDEX_FDM_ID = 10
INDEX_FDM_STATE = 13
INDEX_POS_FLAG = 14

INDEX_RECV_DATA = 20
INDEX_SEND_DATA = 21
INDEX_JOINT_DATA = 22
INDEX_POS_DATA = 22
recv_data = [0, 0, 0, 0]
send_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
joint_data = [0, 0, 0, 0, 0, 0, 0]
pos_data = [0, 0, 0]

class MultiProcessHandle:
    def __init__(self, multi_process, share_memory):
        self.multi_process = multi_process
        self.thread_lock = thread.allocate()
        self.assembly_line_state = STANDBY
        self.share_memory = share_memory

        # 每条流水线一个线程
        for i in range(len(self.multi_process.assembly_line_list)):
            try:
                thread.start_new_thread(self.assembly_line_handle, (self.multi_process.assembly_line_list[i], ))
            except:
                logger.debug("Error: unable to start thread")

    def assembly_line_handle(self, assembly_line):
        index_process = 0
        times = 0
        process_list = []
        process = 0
        assembly_line.state = 1
        while True:
            if assembly_line.state == STANDBY:
                pass

            if assembly_line.state == 1:
                if times == assembly_line.times:
                    assembly_line.state == STANDBY
                else:
                    process_list = assembly_line.process_list
                    times +=1
                    index_process = 0
                    assembly_line.state = 2

            if assembly_line.state == 2:
                if index_process == len(process_list):
                    assembly_line.state = 1
                else:
                    process = process_list[index_process]
                    index_process += 1
                    assembly_line.state = 3

            if assembly_line.state == 3:
                if process.name == "lock":
                    if process.action == "acquire":
                        self.thread_lock.acquire()
                        assembly_line.state = 2
                    if process.action == "release":
                        self.thread_lock.release()
                        assembly_line.state = 2

                if process.name == "move_line":
                    self.share_memory[INDEX_POS_DATA] = process.pos_list
                    self.share_memory[INDEX_POS_FLAG] = SET
                    assembly_line.state = 10

                if process.name == "robot":
                    self.share_memory[INDEX_JOINT_DATA] = process.joint_list
                    self.share_memory[INDEX_JOINT_FLAG] = SET
                    assembly_line.state = 4

                if process.name == "claw":
                    if process.action == "open":
                        self.share_memory[INDEX_CLAW_OPEN_FLAG] = SET
                        assembly_line.state = 5
                    if process.action == "close":
                        self.share_memory[INDEX_CLAW_CLOSE_FLAG] = SET
                        assembly_line.state = 6

                if process.name == "cnc":
                    if process.action == "open":
                        self.share_memory[INDEX_CNC_OPEN_FLAG] = SET
                        assembly_line.state = 7
                    if process.action == "close":
                        self.share_memory[INDEX_CNC_CLOSE_FLAG] = SET
                        assembly_line.state = 8

                if process.name == "fdm":
                    if process.action == "start":
                        self.share_memory[INDEX_FDM_FLAG + assembly_line.id] = SET
                        self.share_memory[INDEX_FDM_ID + assembly_line.id] = assembly_line.id
                        self.share_memory[INDEX_FDM_STATE + assembly_line.id] = SET
                        logger.info("wait fdm: %d print done" % assembly_line.id)
                        print "wait fdm: %d print done" % assembly_line.id
                        assembly_line.state = 9

            if assembly_line.state == 4: # wait joint move
                if self.share_memory[INDEX_JOINT_FLAG] == CLEAR:
                    assembly_line.state = 2

            if assembly_line.state == 5:  # wait claw open
                if self.share_memory[INDEX_CLAW_OPEN_FLAG] == CLEAR:
                    assembly_line.state = 2

            if assembly_line.state == 6:  # wait claw close
                if self.share_memory[INDEX_CLAW_CLOSE_FLAG] == CLEAR:
                    assembly_line.state = 2

            if assembly_line.state == 7:  # wait cnc open
                if self.share_memory[INDEX_CNC_OPEN_FLAG] == CLEAR:
                    assembly_line.state = 2

            if assembly_line.state == 8:  # wait cnc close
                if self.share_memory[INDEX_CNC_CLOSE_FLAG] == CLEAR:
                    assembly_line.state = 2

            if assembly_line.state == 9:  # wait cnc close
                if self.share_memory[INDEX_FDM_STATE + assembly_line.id] == CLEAR:
                    assembly_line.state = 2
                    logger.info("fdm: %d print done" % assembly_line.id)
                    print "fdm: %d print done" % assembly_line.id

            if assembly_line.state == 10: # wait pos move
                if self.share_memory[INDEX_POS_FLAG] == CLEAR:
                    assembly_line.state = 2

class protocol_class:
    def __init__(self, share_memory):
        self.protocol_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.protocol_socket.bind(("127.0.0.1", 12345))
        self.share_memory = share_memory
        self.recv_format = 'BBBB'
        self.send_format = 'BBfffffffffffff'
        self.len_recv = len(self.recv_format)
        self.len_send = len(self.send_format)

        thread.start_new_thread(self.protocol_recv, ())
        thread.start_new_thread(self.protocol_send, ())


    def protocol_recv(self):
        while True:
            pass
            try:
                read_data = self.protocol_socket.recv(1024)
                if self.len_recv == len(read_data):
                    self.share_memory[INDEX_RECV_DATA] = list(unpack(self.recv_format, read_data))
                    self.share_memory[INDEX_RECV_FLAG] = SET
            except:
                pass


    def protocol_send(self):
        while True:
            if self.share_memory[INDEX_SEND_FLAG] == SET:
                self.share_memory[INDEX_SEND_FLAG] = CLEAR
                send_list = self.share_memory[INDEX_SEND_DATA]
                if self.len_send == len(send_list):
                    send_data = pack(self.send_format, *send_list)
                    self.protocol_socket.sendto(send_data, ("127.0.0.1", 56789))



class RobotHandle:
    def __init__(self):
        self.robot_lock = thread.allocate()
        self.robot = robot_init()

    def move_joint(self, joint_list):
        self.robot_lock.acquire()
        logger.info("move_joint")
        self.robot.move_joint(joint_list)
        self.robot_lock.release()

    def move_line(self, pos_list):
        current_pos = self.robot.get_current_waypoint()
        for i in range(3):
            current_pos['pos'][i] += pos_list[i] / 1000
        ik_result = self.robot.inverse_kin(current_pos['joint'], current_pos['pos'], current_pos['ori'])
        logger.info(ik_result)
        joint_radian = ik_result['joint']
        self.robot.move_line(joint_radian)

    def open_claw(self):
        self.robot_lock.acquire()
        self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_00, 1)
        logger.info("open_claw")
        self.robot_lock.release()

    def close_claw(self):
        self.robot_lock.acquire()
        self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_00, 0)
        logger.info("close_claw")
        self.robot_lock.release()

    def open_cnc(self):
        self.robot_lock.acquire()
        self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_01, 1)
        logger.info("open_cnc")
        self.robot_lock.release()

    def close_cnc(self):
        self.robot_lock.acquire()
        logger.info("close_cnc")
        self.robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_01, 0)
        self.robot_lock.release()


def protocol_process(share_memory):
    protocol = protocol_class(share_memory)
    while True:
        pass
        for i in range(3):
            if share_memory[INDEX_FDM_FLAG+i] == SET:
                send_data[0] = 1
                send_data[1] = share_memory[INDEX_FDM_ID + i]
                share_memory[INDEX_SEND_DATA] = send_data
                share_memory[INDEX_FDM_FLAG + i] = CLEAR
                share_memory[INDEX_SEND_FLAG] = SET # 发送

        if share_memory[INDEX_RECV_FLAG] == SET:
            if share_memory[INDEX_RECV_DATA][0] == 0: # data
                for i in range(3):
                    if share_memory[INDEX_RECV_DATA][i+1] == 1:
                        share_memory[INDEX_FDM_STATE+i] = CLEAR
            if share_memory[INDEX_RECV_DATA][0] == 1: #comand
                logger.info("assemble_line start")
                pass
            share_memory[INDEX_RECV_FLAG] = CLEAR

def robot_process(share_memory):
    robot_handle = RobotHandle()
    while True:
        if share_memory[INDEX_JOINT_FLAG] == SET:
            joint_list = share_memory[INDEX_JOINT_DATA][1:7]
            robot_handle.move_joint(joint_list)
            share_memory[INDEX_JOINT_FLAG] = CLEAR

        if share_memory[INDEX_POS_FLAG] == SET:
            pos_list = share_memory[INDEX_POS_DATA]
            robot_handle.move_line(pos_list)
            share_memory[INDEX_POS_FLAG] = CLEAR

        if share_memory[INDEX_CNC_OPEN_FLAG] == SET:
            robot_handle.open_cnc()
            share_memory[INDEX_CNC_OPEN_FLAG] = CLEAR

        if share_memory[INDEX_CNC_CLOSE_FLAG] == SET:
            robot_handle.close_cnc()
            share_memory[INDEX_CNC_CLOSE_FLAG] = CLEAR

        if share_memory[INDEX_CLAW_OPEN_FLAG] == SET:
            robot_handle.open_claw()
            share_memory[INDEX_CLAW_OPEN_FLAG] = CLEAR

        if share_memory[INDEX_CLAW_CLOSE_FLAG] == SET:
            robot_handle.close_claw()
            share_memory[INDEX_CLAW_CLOSE_FLAG] = CLEAR

if __name__ == '__main__':

    manager = Manager()
    share_memory = manager.list()

    for i in range(20):
        share_memory.append(CLEAR)

    share_memory.append(recv_data)
    share_memory.append(send_data)
    share_memory.append(joint_data)
    share_memory.append(pos_data)

    process_robot = Process(target=robot_process, args=(share_memory, ))
    process_robot.start()
    process_protocol = Process(target=protocol_process, args=(share_memory, ))
    process_protocol.start()

    multi_process = parse_xml("process.xml")
    multi_process_handle = MultiProcessHandle(multi_process, share_memory)

    while True:
        pass



