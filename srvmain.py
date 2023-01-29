from echoserver import EchoServer
import socket as sock
from codemaster import generate_cipher
import uuid

class GameServer(EchoServer):
    def __init__(self, addr=None):
        if addr is None:
            super().__init__()
        else:
            super().__init__(addr)

        # user matching memory
        self.matches = {}
        self.to_match = None

        # game storage (user->game, game->word)
        self.gamedata = {}
        self.games = {}

    def start_match(self, p1, p2, game_id):
        quote, code = generate_cipher()
        self.send_msg(p1, code.encode('utf-8'))
        self.send_msg(p2, code.encode('utf-8'))
        self.games[game_id] = quote
        print(
            f"Awaiting answer '{quote}' from players {self.nameof(p1)} and {self.nameof(p2)}"
        )
        
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

            game_id = uuid.uuid1()
            self.gamedata[self.clients[client]] = game_id
            self.gamedata[self.clients[self.to_match]] = game_id
            self.start_match(client, self.to_match, game_id)

            self.to_match = None
    
    def handle_disconnect(self, client: sock.socket):
        if client in self.matches:
            self.matches[client].shutdown(sock.SHUT_RDWR)
            self.matches[client].close()
            self.sockets_list.remove(self.matches[client])
            del self.matches[self.matches[client]]
            del self.matches[client]
        elif client is self.to_match:
            self.to_match = None
    
    def handle_msg(self, client: sock.socket, message: bytes):
        print(f"Got {message.decode('utf-8')} from {self.nameof(client)}")
        if client in self.matches:
            # oof, triple dictionary index
            correct_answer = self.games[self.gamedata[self.clients[client]]]
            user_answer = message.decode('utf-8')
            if correct_answer == 'too_late_so_sad':
                self.send_msg(client, 'too_late'.encode('utf-8'))
                self.start_match(
                    client, self.matches[client], self.gamedata[self.clients[client]])
            elif user_answer == correct_answer:
                self.send_msg(client, 'correct'.encode('utf-8'))
                self.send_msg(self.matches[client], 'too_late'.encode('utf-8'))
                self.games[self.gamedata[self.clients[client]]] = 'too_late_so_sad'
            else:
                self.send_msg(client, 'incorrect'.encode('utf-8'))

if __name__ == "__main__":
    GameServer().run()