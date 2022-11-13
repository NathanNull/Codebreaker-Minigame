# Startup order:
# Server (terminal)
# Client 1 (run)
# Client 2 (second terminal)
# Begin sending moves

from client import Client

me = Client()
start_info = me.recv()
if len(start_info) == 0:
    print("Waiting for opponent")
    start_info = me.wait_recv()
opp = start_info[0]
print(f"Matched with {opp}")
things = ["Rock", "Paper", "Scissors"]

score = [0,0]

running = True
def game_loop():
    plr_input = input("Rock, Paper, or Scissors? (type 'exit' to exit): ").lower()
    if plr_input == "rock":
        plr_input = 0
    elif plr_input == "paper":
        plr_input = 1
    elif plr_input == "scissors":
        plr_input = 2
    elif plr_input == "exit":
        global running
        running = False
        return
    else:
        print("no")
        return

    me.send(str(plr_input))

    msgs = me.recv()
    if len(msgs) == 0:
        print(f"Awaiting {opp}'s move")
        msgs = me.wait_recv()
    opp_input = int(msgs[0])
        
    print(f"{opp} played {things[opp_input]}")

    if plr_input == opp_input:
        print("Draw")
    elif (plr_input - opp_input) % 3 == 1:
        print("You win")
        score[0] += 1
    else:
        print(f"{opp} wins")
        score[1] += 1
    print(f"Current scores: {score[0]}-{score[1]}")

while running:
    game_loop()

me.shutdown(sock.SHUT_RDWR)
me.close()