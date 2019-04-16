import sys

from twisted.internet import reactor, defer, protocol

import config
import json


class ClientProtocol(protocol.DatagramProtocol):

    def __init__(self, msgtype,peer_addresses):
        self.msgtype = msgtype
        self.addrs = dict(peer_addresses)
        for k,v in list(self.addrs.items()):
            self.addrs[v] = k

    def startProtocol(self):
        if self.msgtype == '--master':
            self._send('Z','master_uid',master_id='B')
            reactor.stop()
        if self.msgtype == '--value':
            self._send('Z','current_value',current_value=100)
            reactor.stop()

    def datagramReceived(self, packet, from_addr):
        try:

            message_type, data = packet.split(' ', 1)
            if message_type == 'masterRequest':
                self._send('Z', 'master_uid', master_id='B')

            if message_type == 'resolutionRequest':
                self._send('Z','current_value',current_value=100)
                reactor.stop()

        except Exception:
            print 'Error processing packet: ', packet
            import traceback
            traceback.print_exc()

    def _send(self, to_uid, message_type, **kwargs):
        msg = '{0} {1}'.format(message_type, json.dumps(kwargs))
        print 'snd', to_uid, ':', msg
        self.transport.write(msg, self.addrs[to_uid])


def main():
    reactor.listenUDP(1235, ClientProtocol(sys.argv[1], config.peers))


reactor.callWhenRunning(main)
reactor.run()
