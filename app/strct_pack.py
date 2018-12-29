#!/usr/bin/python
# -*- coding: UTF-8 -*-

from struct import *

pack_list = [1, 2, 3]

pack_data = pack("BBB", *pack_list)

print pack_data
