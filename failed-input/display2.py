from random import randint
from echoserver import EchoServer
from client import Client
from time import sleep
import multiprocessing as mp

input_queue = []

def get_input(callback):
    def async_part():
        print('started callback')
        while not input_queue:
            sleep(0.2)
            print('still going')
        print('input recieved')
        callback(input_queue.pop(0))
    p = mp.Process(target=async_part)
    p.start()
    return p.terminate

def recv_input():
    key = randint(1000, 3000)
    srv = EchoServer(('localhost',key), True)
    print(f"Your key is {key}.")
    def handle_msg(client, msg):
        input_queue.append(msg.decode('utf-8'))
        # confirmation
        srv.send_msg(client, "aeiou".encode('utf-8'))
    srv.handle_msg = handle_msg
    mp.Process(target=srv.run).start()

# call this one in the input terminal
def send_input():
    key = int(input("Enter the key from the other terminal: "))
    c = Client(('localhost', key), 'a')

    while True:
        ipt = input("> ")
        c.send(ipt)
        c.wait_recv()
        print("ok, ready for more")
    
if __name__ == "__main__":
    send_input()