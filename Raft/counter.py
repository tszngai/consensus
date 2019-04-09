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

    def status(self):
        for k, v in self.getStatus().items():
            print('%s: %s' % (str(k), str(v)))

    def leader(self):
        print(self.getStatus()['leader'])

    def state(self):
        print(self.getStatus()['state'])

    def partnerCount(self):
        print(self.getStatus()['partner_nodes_count'])

    def readonlyCount(self):
        print(self.getStatus()['readonly_nodes_count'])

    def unknownCount(self):
        print(self.getStatus()['unknown_connections_count'])

    def logLen(self):
        print(self.getStatus()['log_len'])

    def uptime(self):
        print(self.getStatus()['uptime'])

local = '192.168.1.' + sys.argv[1]

other = ['192.168.1.' + p for p in sys.argv[2:]]

o = CountObj(local, other)
