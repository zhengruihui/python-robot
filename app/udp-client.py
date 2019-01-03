# -*- coding: utf-8 -*-

import socket
import time

'''
客户端使用UDP时，首先仍然创建基于UDP的Socket，然后，不需要调用connect()，直接通过sendto()给服务器发数据：
'''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    time.sleep(1)
    for data in ['a', 'b', 'c']:
        # 发送数据:
        s.sendto(data, ('192.168.1.139', 56789))
        # 接收数据:
s.close()
