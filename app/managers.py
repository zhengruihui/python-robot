# from multiprocessing import Process
# from multiprocessing.managers import BaseManager
# import time
#
# class MemoryShareClass(object):
#     def __init__(self):
#         self.download = [0, 0, 0, 0]
#         self.upload = [0, 0, 0, 0]
#
#
# class MyManager(BaseManager):
#     pass
#
#
#
#
#
# def read(memory_share):
#     while True:
#         for i in range(10):
#             memory_share.upload[i] = i
#
#
# def write(memory_share):
#     while True:
#         for i in range(30):
#             memory_share.download[i] = i
#
#
# if __name__ == '__main__':
#
#     MyManager.register('MemoryShare', MemoryShareClass)
#
#     manager = MyManager()
#     manager.start()
#
#     memory_share = manager.MemoryShare()
#
#     p1 = Process(target=read, args=(memory_share,))
#     p2 = Process(target=read, args=(memory_share,))
#
#     p1.start()
#     p2.start()
#
#     while True:
#         print memory_share.upload
#         print memory_share.download
#         time.sleep(1)

from multiprocessing.managers import BaseManager

class MathsClass(object):
    def __init__(self):
        self.upload = 1

class MyManager(BaseManager):
    pass

MyManager.register('Maths', MathsClass)

if __name__ == '__main__':
    manager = MyManager()
    manager.start()
    maths = manager.Maths()
    print maths.upload         # prints 7
