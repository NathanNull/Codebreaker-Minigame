import socket as sock
import select
import errno
from config import port, HEADERSIZE
import pickle
import sys

class Client:
    def __init__(self):
        uname = input("Username: ")
        
        s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        s.connect(('localhost', port))
        
        s.setblocking(False)
        
        self.sock = s
        self.send(uname)

    def send(self, msg:str):
        """Send a message"""
        msg = msg.encode('utf-8')
        msg_head = f"{len(msg):<{HEADERSIZE}}".encode('utf-8')
        self.sock.send(msg_head + msg)

    def recv(self) -> list[bytes]:
        """Get all messages that have been recieved since last checked"""
        msgs = []
        try:
            while True:
                msg_header = self.sock.recv(HEADERSIZE)
                if not len(msg_header):
                    print("Connection closed by server")
                    sys.exit()

                msg_length = int(msg_header.decode('utf-8').strip())
                message = self.sock.recv(msg_length).decode('utf-8')
                msgs.append(message)
        except IOError as e:
            if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                print(f'Reading error {e}')
                sys.exit()
            return msgs
        except Exception as e:
            print(f'Reading error {e}')
            sys.exit()
    
    def wait_recv(self) -> list[bytes]:
        """Wait until there are messages to get, then return them"""
        msgs = []
        while len(msgs) == 0:
            msgs = self.recv()
        return msgs