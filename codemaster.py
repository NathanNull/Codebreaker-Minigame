import random

letters = 'abcdefghijklmnopqrstuvwxyz'
with open('quotes.txt') as file:
    quotes = [q.split(' ~')[0] for q in file.read().split('\n')]
print(f'{len([q for q in quotes if len(q)<95])} safe quotes')
quotes = ['a']

# simple replacement cipher on one of the quotes
def generate_cipher():
    quote = random.choice(quotes)
    shuffled = list(letters)
    random.shuffle(shuffled)
    cipher = dict(zip(letters, shuffled))
    encoded = ''.join(cipher[l] if l in cipher else l for l in quote)
    return quote, encoded