# consensus
Consensus algorithms in IoT application: A EECE571K Course project

In this work we compare and contrast two consensus protocols, Paxos and Raft, to study how consensus mechanism performs in an IoT setup. Specifically, we build on works from https://github.com/cocagne/multi-paxos-example and https://github.com/bakwc/PySyncObj.

Our experiment setup includes five RPi's as consensus nodes and a Mac workstation as an external client. To rebuild our work, simply clone the repo and run the server Python file on at least three locally connected RPi's. Also run the client file on an external device and make sure it is within the same network as the consensus cluster.
