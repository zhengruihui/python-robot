#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom


class PutPlatform:
    def __init__(self):
        pass


class FDMPrint:
    def __init__(self):
        pass


class CNC:
    def __init__(self):
        pass


class GetPlatform:
    def __init__(self):
        pass


class Start:
    def __init__(self):
        pass


class End:
    def __init__(self):
        pass


class Robot:
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
                    robot.joint_list.append("joint")
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
    return multi_process

