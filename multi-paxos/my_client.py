# This module provides a very simple client interface for suggesting new
# replicated values to one of the servers. No reply is received so an eye must
# be kept on the server output to see if the new suggestion is received. Also,
# when master leases are in use, requests must be sent to the current master
# server. All non-master servers will ignore the requests since they do not have
# the ability to propose new values in the multi-paxos chain.

import sys
import os.path
import argparse
import json
from collections import defaultdict

from twisted.internet import reactor, defer, protocol
from time import sleep

import config

p = argparse.ArgumentParser(description='Multi-Paxos replicated value server')
p.add_argument('cmd', default='PP',choices=['PP', 'LU','PT'], help='PP = Propose, LU = Lookup, PT = PressureTest')
p.add_argument('--v', default=0,help='Enter New Value')

args = p.parse_args()


class ClientProtocol(protocol.DatagramProtocol):

    def __init__(self, cmd,new_value, peer_addresses,client_addresses):
        self.target_addr      = None
        self.new_value = new_value
        self.addrs          = dict(peer_addresses)
        self.masterUid = None
        self.current_value = None
        self.cmd = cmd
        self.uid = 'Z'
        self.peers = peer_addresses
        self.clients = client_addresses
        self.stopflag = False

        # provide two-way mapping between endpoints and server names
        for k,v in list(self.addrs.items()):
            self.addrs[v] = k

        reactor.listenUDP(self.clients[self.uid][1], self)

    def startProtocol(self):
        self.callers = defaultdict(list)
        timer = 0
        for (name, addr) in self.peers.items():
            r = reactor.callLater(timer,self.sendMasterRequest,name)
            self.callers[name].append(r)
            timer = timer + 5

        print("System is waiting for reply...")


    def datagramReceived(self, packet, from_addr):
        try:

            message_type, data = packet.split(' ', 1)
            kwargs = json.loads(data)
            if message_type == 'master_uid':
                if self.masterUid == None:
                    self.masterUid = str(kwargs['master_id'])
                    for caller in self.callers.values():
                        if caller[0].active():
                            caller[0].cancel()
		    print('Current master is ',self.masterUid)
                    self.executeCmd()

            if message_type == 'current_value':
                self.current_value = str(kwargs['current_value'])
                print('Current resolution is ', self.current_value)
                reactor.stop()

        except Exception:
            print 'Error processing packet: ', packet
            import traceback
            traceback.print_exc()

    def stopProtocol(self):
        print('Client stopped.')
    def executeCmd(self):
        if self.masterUid != None:
            if self.cmd == 'PP':
                print("The client is going to propose a value")
                if self.masterUid in self.peers.keys():
                    self.target_addr = self.addrs[self.masterUid]
                    print 'Propose:', self.masterUid, ':', self.new_value
                    self.transport.write('propose {0}'.format(self.new_value), self.target_addr)

                reactor.stop()
            else:
                if self.cmd == 'LU':
                    self._send(self.masterUid,'resolutionRequest')
                    print("THe client is going to look up the resolution")

                else:
                    if self.cmd == 'PT':
                        r = reactor.callLater(65, reactor.stop)
                        while self.stopflag == False:
                            self.new_value = self.new_value + 1
			    self.sendPropose(self.new_value)
			    #self._send(self.masterUid,'masterRequest')
			    sleep(0.0005)

                    else:
                        print("Wrong Command")
        else:
            print('Master ID is missing.')

    def sendMasterRequest(self,to_uid):
        self._send(to_uid,'masterRequest')
    def sendPropose(self,value):
	print 'Propose:', self.masterUid, ':', self.new_value
        self.transport.write('propose {0}'.format(value), self.addrs[self.masterUid])
    def stopprogram(self):
        print(self.new_value)
	reactor.stop()

    def _send(self, to_uid, message_type, **kwargs):
        msg = '{0} {1}'.format(message_type, json.dumps(kwargs))
        print 'snd', to_uid, ':', msg
        self.transport.write(msg, self.addrs[to_uid])


# if len(sys.argv) != 3 or not  sys.argv[1] in config.peers:
#     print('python client.py <A|B|C|D|E> <new_value>')
#     sys.exit(1)

    
def main():
    #reactor.listenUDP(0,ClientProtocol(sys.argv[1], sys.argv[2]))
    c = ClientProtocol(args.cmd, args.v,config.peers, config.clients)
    
reactor.callWhenRunning(main)
reactor.run()

