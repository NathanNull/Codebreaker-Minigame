# Startup order:
# Server (terminal)
# Client 1 (run)
# Client 2 (second terminal)
# Begin sending moves

from client import Client
import socket as sock
from display import get_input, recv_input
recv_input()

me = Client()
start_info = me.recv()
print('info is', start_info)
if start_info is None:
    print('Waiting for opponent')
    start_info = me.wait_recv()
opponent = start_info.decode('utf-8')

score = [0,0]

running = True
def game_loop():
    code = me.wait_recv()
    print(f"Your code is '{code.decode('utf-8')}'.")
    while True:
        print('Your answer: ')
        stop_input = get_input(print)
        print('awaiting response')
        response = me.wait_recv().decode('utf-8')
        if response == 'correct':
            print('You win! Waiting for opponent before starting next round.')
            score[0] += 1
        elif response == 'too_late':
            print('\nYour opponent solved it first. Starting next round. Please press enter to begin.')
            stop_input()
            me.send('beans')
            me.wait_recv()
            score[1] += 1
        else:
            print('That\'s not it, try again.')
            # good old continue-past-the-break
            continue
        break

while running:
    game_loop()

me.shutdown(sock.SHUT_RDWR)
me.close()