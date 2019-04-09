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

ip = '192.168.1.' + sys.argv[1]
port = '8000'

port_other = '8000'

local = ip + ':' + port
other = ['192.168.1.' + p + ':' + port_other for p in sys.argv[2:]]

myObj = CountObj(local, other)
