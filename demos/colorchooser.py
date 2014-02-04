import sys
sys.path.append("../frame_protocol_client")
from BlinkyTape import BlinkyTape, RGB
import tkinter
from tkinter import colorchooser

#You'll need to edit this line to match the
#serial address where your blinkytape is actually attached.
SERIAL_ADDRESS = "COM6"

blinkyTape = None
root = None
try:
    #Create a BlinkyTape client object.
    blinkyTape = BlinkyTape(SERIAL_ADDRESS)
    root = tkinter.Tk()
    
    #Initiate the tape's brightness. 10 is a pretty good setting
    #for developing in a dim room without burning your eyes out!
    #Edit this upward to display the clock in brighter-lit areas.
    blinkyTape.setBrightness(40)

    while True:
        color = colorchooser.askcolor()[0]
        if not color:
            break
        color = RGB(int(color[0]), int(color[1]), int(color[2]))
        blinkyTape.setColor(color);
finally:
    if root:
        root.destroy()
    if blinkyTape:
        #If the program exits the infinite loop controllably (e.g. by
        #keyboard interrupt exception) politely reset the blinkytape to
        #its initial state.
        blinkyTape.reset()
