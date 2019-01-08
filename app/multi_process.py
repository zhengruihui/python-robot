#!/usr/bin/python
# -*- coding: UTF-8 -*-

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


INDEX_RECV_DATA = 20
INDEX_SEND_DATA = 21
INDEX_JOINT_DATA = 22
recv_data = [0, 0, 0, 0]
send_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
joint_data = [0, 0, 0, 0, 0, 0, 0]

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
                    assembly_line.state = 2

            if assembly_line.state == 2:
                if index_process == len(process_list):
                    assembly_line.state = 1
                else:
                    process = process_list[index_process]
                    index_process += 1
                    assembly_line.state = 3

            if assembly_line.state == 3:
                if process.name == "start":
                    if process.lock == "true":
                        self.thread_lock.acquire()
                        assembly_line.state = 2

                if process.name == "end":
                    if process.lock == "false":
                        self.thread_lock.release()
                        assembly_line.state = 2

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

                if process.name == "fdm_print":
                    self.share_memory[INDEX_FDM_FLAG + assembly_line.id] = SET
                    self.share_memory[INDEX_FDM_ID + assembly_line.id] = assembly_line.id
                    self.share_memory[INDEX_FDM_STATE + assembly_line.id] = SET
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
                    print "fdm: %d print done" % assembly_line.id
