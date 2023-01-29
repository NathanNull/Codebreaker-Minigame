import socket as sock
import select
from config import port, HEADERSIZE
import uuid

class EchoServer:
    def __init__(self, addr = ("localhost", port), silent=False):
        s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen()

        self.server_socket = s
        self.sockets_list = [s]
        self.clients = {}
        self.unames = {}

        if not silent:
            print(f"Server online at {addr[0]}:{addr[1]}")
        self.silent = silent

    def recv_msg(self, client: sock.socket):
        try:
            msg_header = client.recv(HEADERSIZE)
            if not len(msg_header):
                return False
            msg_length = int(msg_header.decode('utf-8').strip())
            return {'header': msg_header, 'data': client.recv(msg_length)}
        except sock.error:
            return False
    
    def send_msg(self, client: sock.socket, msg: bytes):
        msg_head = f"{len(msg):<{HEADERSIZE}}".encode('utf-8')
        client.send(msg_head + msg)
    
    def nameof(self, client: 'sock.socket | uuid.UUID') -> str:
        if isinstance(client, sock.socket):
            client = self.clients[client]
        return self.unames[client]

    def run(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    # New client has connected to the server
                    client_socket, client_addr = self.server_socket.accept()

                    user = self.recv_msg(client_socket)
                    if user is False:
                        continue
                    
                    self.sockets_list.append(client_socket)
                    client_id = uuid.uuid1()
                    self.clients[client_socket] = client_id
                    self.unames[client_id] = user['data'].decode('utf-8')
                    self.handle_connect(client_socket, str(client_addr), user['data'])
                else:
                    # Recieving message from preexisting client
                    message = self.recv_msg(notified_socket)
                    if message is False:
                        if not self.silent:
                            print(f"Closed connection from {self.nameof(notified_socket)}")
                        self.sockets_list.remove(notified_socket)
                        del self.unames[self.clients[notified_socket]]
                        del self.clients[notified_socket]
                        self.handle_disconnect(notified_socket)
                        continue
                    self.handle_msg(notified_socket, message['data'])
                            
            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.unames[self.clients[notified_socket]]
                del self.clients[notified_socket]
                self.handle_disconnect(notified_socket)
    
    def handle_msg(self, client:sock.socket, message: bytes):
        if not self.silent:
            print(
                f"Recieved from {self.nameof(client)}: {message.decode('utf-8')}"
            )
        for other_client in self.clients:
            if other_client != client:
                user = self.clients[client]
                self.send_msg(other_client, user)
                self.send_msg(other_client, message)
    
    def handle_connect(self, client:sock.socket, addr: str, user_data:bytes):
        if not self.silent:
            print(f"accepted from {addr}, uname: {user_data.decode('utf-8')}")
    
    def handle_disconnect(self, client: sock.socket):
        pass

if __name__ == "__main__":
    server = EchoServer()
    server.run()