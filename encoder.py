from digitalio import DigitalInOut, Direction, Pull

class Encoder:
    
    """
    CircuitPython Rotary Encoder (without interrupts)
    2017_10_16 Andy Clymer
    
    from encoder import Encoder
    e = Encoder(board.D0, board.D2)
    while True:
        encoderValue = e.read()
        if encoderValue:
            print(encoderValue)
    """
    
    def __init__(self, pin1, pin2):
        # Init pins
        self.d1 = DigitalInOut(pin1)
        self.d1.direction = Direction.INPUT
        self.d1.pull = Pull.UP
        self.d2 = DigitalInOut(pin2)
        self.d2.direction = Direction.INPUT
        self.d2.pull = Pull.UP
        # Values for comparison
        self.prev1 = 0
        self.prev2 = 0
        self.new1 = 0
        self.new2 = 0
        self.lastFewDirs = [0, 0, 0, 0]
        # Encoder truth table
        self.encTable = {
            (1, 1): {(1, 0):1, (1, 1):0, (0, 1):-1, (0, 0):2},
            (1, 0): {(0, 0):1, (1, 0):0, (1, 1):-1, (0, 1):2},
            (0, 0): {(0, 1):1, (0, 0):0, (1, 0):-1, (1, 1):2},
            (0, 1): {(1, 1):1, (0, 1):0, (0, 0):-1, (1, 0):2}}
            
    def read(self):
        self.new1 = self.d1.value
        self.new2 = self.d2.value
        # Pin values changed:
        if not (self.prev1, self.prev2) == (self.new1, self.new2):
            # Determine out the dirction
            newDir = self.encTable[(self.prev1, self.prev2)][(self.new1, self.new2)]
            self.prev1 = self.new1
            self.prev2 = self.new2
            # Hold on to this new direction with the last three
            self.lastFewDirs = self.lastFewDirs[1:] + [newDir]
            # A good reading has four values of the same direction.
            # If the list adds up as expected, return the direction and rest the list
            s = sum(self.lastFewDirs)
            if s == 4:
                self.lastFewDirs = [0, 0, 0, 0]
                return 1
            elif s == -4:
                self.lastFewDirs = [0, 0, 0, 0]
                return -1
        return None