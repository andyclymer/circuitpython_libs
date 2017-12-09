# CircuitPython Encoder

A simple rotary encoder object for CircuitPython, without using interrupts. The common pin of the encoder is connected to GND and pins A and B are connected to two digital IO pins.

```python
import board
from encoder import Encoder

def movedUp():
    print("Up!")
    
def movedDown():
    print("Down!")
    
e = Encoder(board.D0, board.D4, upCallback=movedUp, downCallback=movedDown)

# Main Loop:
while True:
    e.update()
```