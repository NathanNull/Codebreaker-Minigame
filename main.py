# Startup order:
# Server
# Client 1 (run)
# Client 2 (second terminal)
# Begin sending moves

from client import Client

me = Client()
things = ["Rock", "Paper", "Scissors"]

def game_loop():
  plr_input = input("Rock, Paper, or Scissors?: ").lower()
  if plr_input == "rock":
    plr_input = 0
  elif plr_input == "paper":
    plr_input = 1
  elif plr_input == "scissors":
    plr_input = 2
  else:
    print("no")
    return

  me.send(str(plr_input))

  while True:
      msgs = me.recv()
      if len(msgs) > 0:
          break
  opp_input = int(msgs[0][1])
  print(opp_input)
      
  print(f"Opponent played {things[opp_input]}")

  if plr_input == opp_input:
    print("Draw")
  elif (plr_input - opp_input) % 3 == 1:
    print("You win")
  else:
    print("Opponent wins")

while True:
    game_loop()