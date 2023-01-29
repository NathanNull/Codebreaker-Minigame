import socket as sock
import errno
from config import port, HEADERSIZE
import sys

class Client:
    def __init__(self, addr=('localhost', port), uname=None):
        if uname is None:
            uname = input("Username: ")
        
        s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        s.connect(addr)
        
        s.setblocking(False)
        
        self.sock = s
        self.send(uname)

    def send(self, msg:str):
        """Send a message"""
        msg = msg.encode('utf-8')
        msg_head = f"{len(msg):<{HEADERSIZE}}".encode('utf-8')
        self.sock.send(msg_head + msg)

    def recv(self) -> 'bytes | None':
        """Get a single message, or None if there isn't one"""
        try:
            msg_header = self.sock.recv(HEADERSIZE)
            if not len(msg_header):
                print("Connection closed by server")
                sys.exit()

            msg_length = int(msg_header.decode('utf-8').strip())
            msg = self.sock.recv(msg_length)
            if msg.decode('utf-8') == "__shutdown__or__something__":
                print("Connection closed by server")
                sys.exit()
            return msg
        except IOError as e:
            if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                print(f'Reading error {e}')
                sys.exit()
            return None
        except Exception as e:
            print(f'Reading error {e}')
            sys.exit()
    
    def wait_recv(self) -> bytes:
        """Wait until there's a message to get, then return it"""
        msg = None
        while msg is None:
            msg = self.recv()
        return msg