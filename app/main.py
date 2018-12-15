#!/usr/bin/python
# -*- coding: UTF-8 -*-

import robot
import thread
import time


# 为线程定义一个函数
def print_time(thread_name, delay):
    count = 0
    while True:
        time.sleep(delay)
        count += 1
        print "%s: %s" % (thread_name, time.ctime(time.time()))


print "Hello word!"

employee = robot.Employee("zhengruihui", 31)
employee.display_employee()

# 创建两个线程
try:
    thread.start_new_thread(print_time, ("Thread-1", 2,))
    thread.start_new_thread(print_time, ("Thread-2", 4,))
except:
    print "Error: unable to start thread"

import Tkinter
top = Tkinter.Tk()
# 进入消息循环
top.mainloop()


while 1:
   pass