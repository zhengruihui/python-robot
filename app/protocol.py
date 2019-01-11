#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser


config = ConfigParser.ConfigParser()
config.readfp(open('resources/config_pack.ini'))
a = config.get("axis1","max_acce")
print a