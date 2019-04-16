
# (IP,UDP Port Number)
peers = dict( A=('192.168.1.74',1234),
              B=('192.168.1.75',1235),
              C=('192.168.1.76',1236),
              D=('192.168.1.66',1237),
              E=('192.168.1.79',1238))

#S=('192.168.1.66',1236))


clients = dict(Z=('192.168.1.74',1240))

# State files for crash recovery. Windows users will need to modify
# these.
state_files = dict( A='/tmp/A.json',
                    B='/tmp/B.json',
                    C='/tmp/C.json',
                    D='/tmp/D.json',
                    E='/tmp/E.json',)
