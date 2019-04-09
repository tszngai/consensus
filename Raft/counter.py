import sys
import time
from functools import partial
sys.path.append("../")
from pysyncobj import SyncObj, replicated, config

class CountObj(SyncObj):

    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(CountObj, self).__init__(selfNodeAddr, otherNodeAddrs, conf=config.SyncObjConf(dynamicMembershipChange=True))
        self.__counter = 0

    @replicated
    def inc(self):
        self.__counter += 1
        return self.__counter

    @replicated
    def add(self, value):
        self.__counter += value
        return self.__counter
    
    @replicated
    def dec(self):
        self.__counter -= 1
        return self.__counter
    
    @replicated
    def sub(self, value):
        self.__counter -= value
        return self.__counter

    def getCounter(self):
        return self.__counter

local = '192.168.1.' + sys.argv[1]

other = ['192.168.1.' + p for p in sys.argv[2:]]

o = CountObj(local, other)
