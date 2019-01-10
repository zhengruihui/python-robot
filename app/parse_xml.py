#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom


class FDM:
<<<<<<< HEAD
    def __init__(self):
        pass

class Motion:
=======
>>>>>>> 84e1d9d1d28168b78ac64282519a57a368d17c85
    def __init__(self):
        pass

class CNC:
    def __init__(self):
        pass


class Claw:
    def __init__(self):
        pass


class Lock:
    def __init__(self):
        pass


class Robot:
    def __init__(self):
        pass

class MoveLine:
    def __init__(self):
        pass

class AssemblyLine:
    def __init__(self):
        pass


class MultiProcess:
    def __init__(self):
        pass


def parse_xml(xml_name):
    # 使用minidom解析器打开 XML 文档
    multi_process = MultiProcess()
    dom_tree = xml.dom.minidom.parse(xml_name)
    multi_process_xml = dom_tree.documentElement
    multi_process.assembly_line_list = []
    multi_process.name = multi_process_xml.getAttribute("name")
    assembly_line_xml_list = multi_process_xml.getElementsByTagName("assembly_line")
    for assembly_line_xml in assembly_line_xml_list:
        assembly_line = AssemblyLine()
        assembly_line.process_list = []
        assembly_line.state = 0
        assembly_line.id = int(assembly_line_xml.getAttribute("id"))
        assembly_line.times = int(assembly_line_xml.getAttribute("times"))
        multi_process.assembly_line_list.append(assembly_line)
        child_list = assembly_line_xml.childNodes
        for child in child_list:    # level 0
            if child.nodeType == child.ELEMENT_NODE:
                if child.nodeName == "lock":
                    lock = Lock()
                    lock.name = child.nodeName
                    lock.action = child.getAttribute("action")
                    assembly_line.process_list.append(lock)

                if child.nodeName == "move_line":
                    move_line = MoveLine()
                    move_line.name = child.nodeName
                    move_line.pos_list = []
<<<<<<< HEAD
                    move_line.pos_list.append(float(child.getAttribute("x")) / 1000)
                    move_line.pos_list.append(float(child.getAttribute("y")) / 1000)
                    move_line.pos_list.append(float(child.getAttribute("z")) / 1000)
                    assembly_line.process_list.append(move_line)

                if child.nodeName == "motion":
                    motion = Motion()
                    motion.name = child.nodeName
                    motion.axis_list = []
                    motion.axis_list.append(float(child.getAttribute("x")))
                    motion.axis_list.append(float(child.getAttribute("y")))
                    motion.action = child.getAttribute("action")
                    assembly_line.process_list.append(motion)
=======
                    move_line.pos_list.append(float(child.getAttribute("x")))
                    move_line.pos_list.append(float(child.getAttribute("y")))
                    move_line.pos_list.append(float(child.getAttribute("z")))
                    assembly_line.process_list.append(move_line)
>>>>>>> 84e1d9d1d28168b78ac64282519a57a368d17c85

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

                if child.nodeName == "claw":
                    claw = Claw()
                    claw.name = child.nodeName
                    claw.action = child.getAttribute("action")
                    assembly_line.process_list.append(claw)

                if child.nodeName == "fdm":
                    fdm = FDM()
                    fdm.name = child.nodeName
                    fdm.action = child.getAttribute("action")
                    assembly_line.process_list.append(fdm)

                if child.nodeName == "cnc":
                    cnc = CNC()
                    cnc.name = child.nodeName
                    cnc.action = child.getAttribute("action")
                    assembly_line.process_list.append(cnc)
    return multi_process

