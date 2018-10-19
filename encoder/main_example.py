import board
from encoder import Encoder

def movedUp():
	print("Up!")
def movedDown():
	print("Down!")

e = Encoder(board.D0, board.D4, upCallback=movedUp, downCallback=movedDown)
while True:
	e.update()