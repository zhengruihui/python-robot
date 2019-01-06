#!/usr/bin/python
# -*- coding: UTF-8 -*-
import multiprocessing
import time


class ClockProcess(multiprocessing.Process,):
    def __init__(self, name):
        multiprocessing.Process.__init__(self)
        self.name = name

    def run(self):
        while True:
            print self.name
            time.sleep(1)


if __name__ == '__main__':
    name_list = ["A", "B", "C"]
    for name in name_list:
        p = ClockProcess(name)
        p.start()

