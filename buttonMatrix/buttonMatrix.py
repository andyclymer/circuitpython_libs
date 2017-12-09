import board
from digitalio import DigitalInOut, Direction, Pull

class Button(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.sPin = None
        self.rPin = None
        self.downCback = None
        self.upCback = None
        self.holdCbk = None
        self.id = None
        self.state = False
        self.tSinceChange = 0
        self.tSinceRepeat = 0
        
    def update(self):
        # Find if up, down, changed. If down for a length of time, call the hold
        os = self.state
        self.sPin.value = True
        ns = self.rPin.value
        if not os == ns:
            i = dict(buttonID=self.id)
            if ns == True:
                if self.downCback: self.downCback(info=i)
                if self.parent.downCback: self.parent.downCback(info=i)
            else:
                if self.upCback: self.upCback(info=i)
                if self.parent.upCback: self.parent.upCback(info=i)
        self.state = ns
        self.sPin.value = False
        
        

class ButtonMatrix:
    """
    Controller for a matrix of buttons.
    Each button is connected to a "send" and "receive" pin
    
        buttonMap = [
            dict(sPinName="D0", rPinName="D2", btnID=1),
            dict(sPinName="D0", rPinName="D4", btnID=2)]
        Matrix = ButtonMatrix(buttonMap)
    
    """
    def __init__(
            self, 
            buttonMap=[], 
            keyDownCallback=None, 
            keyUpCallback=None, 
            keyHoldCallback=None, 
            debounceTime=0, 
            holdDelayTime=1000, 
            holdRepeatTime=250):
        # Cbks
        self.downCback = keyDownCallback
        self.upCback = keyUpCallback
        self.holdCbk = keyHoldCallback
        # Buttons and pins
        self._buttons = [] # List of button objects
        self._pinMap = {} # Each pin name, mapped to a pin object, for easier button setup
        # Debounce and hold times
        self.debounceTime = debounceTime 
        self.holdDelayTime = holdDelayTime 
        self.holdRepeatTime = holdRepeatTime
        # Initialize
        self.initPins(buttonMap)
    
    def initPins(self, buttonMap):
        # Initialize pins and make Button objects
        for item in buttonMap:
            button = Button(self)
            button.id = item.get("buttonID", None)
            button.downCback = item.get("keyDownCallback", None)
            button.upCback = item.get("keyUpCallback", None)
            button.holdCbk = item.get("keyHoldCallback", None)
            if not item["sendPinName"] in self._pinMap:
                sPin = DigitalInOut(getattr(board, item["sendPinName"]))
                sPin.direction = Direction.OUTPUT
                self._pinMap[item["sendPinName"]] = sPin
            button.sPin = self._pinMap[item["sendPinName"]]
            if not item["receivePinName"] in self._pinMap:
                rPin = DigitalInOut(getattr(board, item["receivePinName"]))
                rPin.direction = Direction.INPUT
                rPin.pull = Pull.DOWN
                self._pinMap[item["receivePinName"]] = rPin
            button.rPin = self._pinMap[item["receivePinName"]]
            self._buttons.append(button)
    
    def update(self):
        # Check each button object
        for button in self._buttons:
            button.update()
          
          