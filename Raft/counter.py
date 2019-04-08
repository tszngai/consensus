import sys
import time
from functools import partial
sys.path.append("../")
from pysyncobj import SyncObj, replicated

class CountObj(SyncObj):

    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(CountObj, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.__counter = 0

    @replicated
    def incCounter(self):
        self.__counter += 1
        return self.__counter

    @replicated
    def addValue(self, value):
        self.__counter += value
        return self.__counter
    
    @replicated
    def decCounter(self):
        self.__counter -= 1
        return self.__counter
    
    @replicated
    def subValue(self, value):
        self.__counter -= value
        return self.__counter

    def getCounter(self):
        return self.__counter

ip = '192.168.1.75'
port = '8000'

ip_other = '192.168.1.78'
port_other = '8000'

local = ip + ':' + port
other = [ip_other + ':' + port_other]

myObj = CountObj(local, other)
