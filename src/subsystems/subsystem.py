

import threading
from threading import Thread
import time


class subsystem:

    def __init__(self, name:str, shouldStart:bool=True, loopTime:int=20):
        self.thread:Thread=None # type: ignore
        self.shouldLive=False
        self.name=name
        self.loopTime=loopTime
        if shouldStart:

            self.start()


    def start(self):
        self.thread=threading.Thread(target=self.loop, daemon=True)
        self.shouldLive=True
        self.thread.start()

    def loop(self):
        while (self.shouldLive):

            timestamp = time.time()
            self.main()
            if (timestamp + self.loopTime/1000 >= time.time()):
                time.sleep(time.time()+self.loopTime/1000 - timestamp)
            else:
                print("Loop overrun in subsystem", self.name, "by", -1000*(time.time()+self.loopTime/1000 - timestamp),"MS")

    def main(self):
        print("subsystem", self.name, "is running with no definition of main")

    def kill(self):
        self.shouldLive=False

    def isAlive(self)->bool:
        return self.thread!=None and self.thread.is_alive() # type: ignore


