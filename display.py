# import curses
# import multiprocessing as mp
#
# input_box = None
# screen = None
# text_box = None
#
# def dprint(str):
#     pos = list(text_box.getyx())
#     w = text_box.getmaxyx()[1]
#     for char in str:
#         text_box.addch(char)
#         pos[1] += 1
#         if pos[1] >= w:
#             pos[1] = 0
#             pos[0] += 1
#     text_box.move(*pos)
#     text_box.cursyncup()
#
# def get_input(callback):
#     def ipt():
#         line = ""
#         while True:
#             pos = screen.getyx()
#             screen.addstr(str(pos))
#             screen.refresh()
#             c = screen.getch()
#             if c == 127:
#                 line = line[:-1]
#                 input_box.clear()
#                 input_box.addstr(line)
#                 input_box.refresh()
#             elif c == 10:
#                 input_box.clear()
#                 input_box.refresh()
#                 return callback(line)
#             else:
#                 line = line+chr(c)
#                 input_box.addch(chr(c))
#                 input_box.refresh()
#             screen.move(*pos)
#             screen.refresh()
#     p = mp.Process(target=ipt)
#     p.start()
#     return p.terminate

# def main(scr):
#     global screen
#     screen = scr
#     h, w = scr.getmaxyx()

#     curses.curs_set(1)
    
#     global text_box
#     text_box = curses.newwin(h-5, w)

#     line = curses.newwin(1, w, h-5, 0)
#     line.addstr('-'*(w-1))
#     line.refresh()
    
#     global input_box
#     input_box = curses.newwin(4, w, h-4, 0)
#     input_box.refresh()
    
#     do_ipt = True
#     while True:
#         if do_ipt:
#             do_ipt = False
#             def l(i):
#                 nonlocal do_ipt
#                 do_ipt = True
#                 text_box.addstr(i)
#                 text_box.refresh()
#             get_input(l)
#         dprint("ae")
#         text_box.refresh()
#         curses.napms(200)
# curses.wrapper(main)

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