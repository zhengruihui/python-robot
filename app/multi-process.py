# !/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom


class GoHome:
    def __init__(self):
        pass


class AssemblyLine:
    def __init__(self):
        pass


class GetPlatform:
    def __init__(self):
        pass


class MultiProcess:
    def __init__(self):
        pass


if __name__ == '__main__':

    # multi_process = MultiProcess()

    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse("process.xml")
    multi_process = DOMTree.documentElement
    if multi_process.hasAttribute("name"):
        print "Root element : %s" % multi_process.getAttribute("name")

    # 在集合中获取所有流水线
    assembly_line_list = multi_process.getElementsByTagName("assembly_line")
    for assembly_line in assembly_line_list:
        print assembly_line.getAttribute("id")
        print assembly_line.getAttribute("times")

        get_platform_list = assembly_line.getElementsByTagName("get_platform")
        for get_platform in get_platform_list:
            motion_list = get_platform.getElementsByTagName("motion")
            for motion in motion_list:
                print motion.getAttribute("comment")
                child_list = motion.childNodes
                for child in child_list:
                    print child.nodeValue

            coordidate_list = get_platform.getElementsByTagName("coordidate")
            for coordidate in coordidate_list:
                print coordidate.getAttribute("joint1")
                print coordidate.getAttribute("joint2")
                print coordidate.getAttribute("joint3")
                print coordidate.getAttribute("joint4")
                print coordidate.getAttribute("joint5")
                print coordidate.getAttribute("joint6")

    print "parse done"





