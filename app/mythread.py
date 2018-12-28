import threading
import time


class Job(threading.Thread):

    def __init__(self, name, sleep_time):
        super(Job, self).__init__()
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        self.name = name
        self.sleep_time = sleep_time

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            print "thread_name: %s" % self.name
            time.sleep(int(self.sleep_time))

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()


a_thread = Job("a_thread", 1)
a_thread.start()
b_thread = Job("b_thread", 3)
b_thread.start()
a_thread.pause()
time.sleep(5)
a_thread.resume()
b_thread.stop()