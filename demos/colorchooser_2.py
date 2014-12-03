import sys
sys.path.append("../frame_protocol_client")
from BlinkyTape_2 import BlinkyTape, RGB
from Tkinter import *
from tkColorChooser import askcolor

#You'll need to edit this line to match the
#serial address where your blinkytape is actually attached.
SERIAL_ADDRESS = "/dev/tty.usbmodem14121"

#Blinkytape gets bright! 10 is a pretty good setting
#for developing in a dim room without burning your eyes out.
BRIGHTNESS = 10

blinkyTape = None
root = None

try:
    #Create a BlinkyTape client object.
    blinkyTape = BlinkyTape(SERIAL_ADDRESS)

    #Initiate the tape's brightness.
    blinkyTape.setBrightness(BRIGHTNESS)

    def getColor():
        color = askcolor()
        print color

        color = RGB(int(color[0][0]), int(color[0][1]), int(color[0][2]))
        blinkyTape.setColor(color);

    Button(text='Select Color', command=getColor).pack()
    mainloop()
finally:
    if blinkyTape:
        #If the program exits the infinite loop controllably (e.g. by
        #keyboard interrupt exception) politely reset the blinkytape to
        #its initial state.
        blinkyTape.reset()
