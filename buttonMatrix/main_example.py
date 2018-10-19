import board
from digitalio import DigitalInOut, Direction, Pull
from buttonMatrix import ButtonMatrix

def buttonDownCallback(info):
	print("Button _down_", info)

def buttonUpCallback(info):
	print("Button ^UPUP^", info)

def buttonHoldCallback(info):
	print("Button hold", info)
	
buttonMap = [
	dict(sendPinName="D0", receivePinName="D2", buttonID=1),
	dict(sendPinName="D1", receivePinName="D2", buttonID=2),
	dict(sendPinName="D0", receivePinName="D4", buttonID=3),
	dict(sendPinName="D1", receivePinName="D4", buttonID=4),
	dict(sendPinName="D0", receivePinName="D3", buttonID=5),
	dict(sendPinName="D1", receivePinName="D3", buttonID=6)]

Matrix = ButtonMatrix(
			buttonMap, 
			keyDownCallback=buttonDownCallback, 
			keyUpCallback=buttonUpCallback, 
			keyHoldCallback=buttonHoldCallback, 
			holdDelayTime=1, 
			holdRepeatTime=0.1)

# Main Loop
while True:
	Matrix.update()