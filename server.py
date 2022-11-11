import socket as sock
import select
import time
from threading import Thread
from config import port
import pickle

HEADERSIZE = 10

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
s.bind(("localhost", port))
s.listen()

sockets_list = [s]
clients = {}

def recv_msg(client):
    try:
        msg_header = client.recv(HEADERSIZE)
        if not len(msg_header):
            return False
        msg_length = int(msg_header.decode('utf-8').strip())
        return {'header': msg_header, 'data': client.recv(msg_length)}
    except sock.error:
        return False

def format_msg(msg):
    return bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+pickle.dumps(msg)

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == s:
            client_socket, client_addr = s.accept()

            user = recv_msg(client_socket)
            if user is False:
                continue
            
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f"accepted from {client_addr}, uname: {user['data'].decode('utf-8')}")
        else:
            message = recv_msg(notified_socket)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(
                f"Recieved from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}"
            )
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        user['header']+user['data']+message['header']+message['data']
                    )
                    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

