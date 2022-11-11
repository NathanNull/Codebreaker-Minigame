import socket as sock
import select
import errno
from config import port
import pickle
import sys

HEADERSIZE = 10

class Client:
    def __init__(self):
        uname = input("Username: ")
        
        s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        s.connect(('localhost', port))
        
        s.setblocking(False)
        
        username = uname.encode('utf-8')
        username_header = f"{len(username):<{HEADERSIZE}}".encode('utf-8')
        s.send(username_header+username)
        self.sock = s

    def send(self, msg):
        if msg:
            msg = msg.encode('utf-8')
            msg_head = f"{len(msg):<{HEADERSIZE}}".encode('utf-8')
            self.sock.send(msg_head + msg)

    def recv(self):
        msgs = []
        try:
            while True:
                username_header = self.sock.recv(HEADERSIZE)
                if not len(username_header):
                    print("Connection closed by server")
                    sys.exit()
                uname_length = int(username_header.decode('utf-8').strip())
                username = self.sock.recv(uname_length).decode('utf-8')
    
                msg_header = self.sock.recv(HEADERSIZE)
                msg_length = int(msg_header.decode('utf-8').strip())
                message = self.sock.recv(msg_length).decode('utf-8')
                msgs.append([username, message])
        except IOError as e:
            if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                print(f'Reading error {e}')
                sys.exit()
            return msgs
        except Exception as e:
            print(f'Reading error {e}')
            sys.exit()