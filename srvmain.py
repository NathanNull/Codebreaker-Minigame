from echoserver import EchoServer
import socket as sock

class RPSServer(EchoServer):
    def __init__(self, addr=None):
        if addr is None:
            super().__init__()
        else:
            super().__init__(addr)

        self.matches = {}
        self.to_match = None

    def handle_connect(self, client: sock.socket, addr: str, user_data: bytes):
        print(f"{user_data.decode('utf-8')} has connected from {addr}")
        if self.to_match is None:
            # Await another connection for match
            self.to_match = client
        else:
            # Match clients
            self.matches[self.to_match] = client
            self.matches[client] = self.to_match
            print(f"Matched {self.nameof(client)} with {self.nameof(self.to_match)}")
            self.send_msg(client, self.nameof(self.to_match).encode('utf-8'))
            self.send_msg(self.to_match, self.nameof(client).encode('utf-8'))
            self.to_match = None
    
    def handle_disconnect(self, client: sock.socket):
        if client in self.matches:
            self.matches[client].shutdown(sock.SHUT_RDWR)
            self.matches[client].close()
            self.sockets_list.remove(self.matches[client])
            del self.matches[self.matches[client]]
            del self.matches[client]
    
    def handle_msg(self, client: sock.socket, message: bytes):
        print(f"Got {message.decode('utf-8')} from {self.nameof(client)}")
        if client in self.matches:
            print(f"Sending message to {self.nameof(self.matches[client])}")
            self.send_msg(self.matches[client], message)

if __name__ == "__main__":
    RPSServer().run()