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

    multi_process = MultiProcess()

    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse("process.xml")
    multi_process = DOMTree.documentElement
    if multi_process.hasAttribute("name"):
        print "Root element : %s" % multi_process.getAttribute("name")

    # 在集合中获取所有流水线
    assembly_lines = multi_process.getElementsByTagName("assembly_line")

    for assembly_line in assembly_lines:
        print assembly_line.getAttribute("id")
        print assembly_line.getAttribute("times")

        get_platform = assembly_line.getElementsByTagName("get_platform")[0]
        motion = get_platform.getElementsByTagName("motion")[0]
        print motion.getAttribute("comment")
        print motion.childNodes[0].data


    print "parse done"



