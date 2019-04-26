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

import config
import collections

from composable_paxos import ProposalID, Accepted,PaxosMessage



class DummyEnemyProtocol(protocol.DatagramProtocol):

    def __init__(self, peer_addresses):
        self.addrs = dict(peer_addresses)
        self.final_value = None
        self.uid = 'S'
        self.peers = peer_addresses

        # provide two-way mapping between endpoints and server names
        for k, v in list(self.addrs.items()):
            self.addrs[v] = k

        reactor.listenUDP(self.peers[self.uid][1], self)

    def startProtocol(self):
        print("Start Evasdropping...")

    def datagramReceived(self, packet, from_addr):
        try:

            message_type, data = packet.split(' ', 1)
            kwargs = json.loads(data)
            if message_type != 'propose':
                try:
                    from_uid = self.addrs[from_addr]
                except Exception:
                    from_uid = "UNK"

                print
                'rcv', from_uid, ':', packet

                handler = getattr(self, 'receive_' + message_type, None)

                if handler:
                    kwargs = json.loads(data)

                    for k in kwargs.keys():
                        if k.endswith('_id') and kwargs[k] is not None:
                            # JSON encodes the proposal ids as lists,
                            # composable-paxos requires requires ProposalID instances
                            kwargs[k] = ProposalID(*kwargs[k])

                    handler(from_uid, **kwargs)
        except Exception:
            print
            'Error processing packet: ', packet
            import traceback
            traceback.print_exc()

    def stopProtocol(self):
        print('Client stopped.')



    def receive_accepted(self, from_uid, instance_number, proposal_id, proposal_value):
        # Only process messages for the current link in the multi-paxos chain
        msg = Accepted(from_uid, proposal_id, proposal_value)
        print("Evasdroping succeeded: The proposal value is ", msg.proposal_value)



# if len(sys.argv) != 3 or not  sys.argv[1] in config.peers:
#     print('python client.py <A|B|C|D|E> <new_value>')
#     sys.exit(1)


def main():
    # reactor.listenUDP(0,ClientProtocol(sys.argv[1], sys.argv[2]))
    c = DummyEnemyProtocol(config.peers)


reactor.callWhenRunning(main)
reactor.run()

