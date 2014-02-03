import sys
sys.path.append("../frame_protocol_client")
from BlinkyTape import BlinkyTape
from datetime import datetime
from time import sleep

#You'll need to edit this line to match the
#serial address where your blinkytape is actually attached.
SERIAL_ADDRESS = "COM6"

#Encodes an integer (num) into a fixed-length (numBits) array of color
#codes representing 1 (onColor) and 0 (offColor) bits
def encode_to_led_bits(num, numBits, onColor, offColor):
    byts = []
    #Mask off the binary bits of num to individually translate
    #them into "on" and "off"
    for i in [2**n for n in range(numBits)]:
        if num & i == 0:
            byts.append(offColor)
        else:
            byts.append(onColor)
    return byts

#Reads the current wall time and encodes it into an array of LED color values
#representing binary bits.
def encode_time():
    now = datetime.now()
    #Hours, in 24hr time. Deep blue for on, pale blue for off. Five bits wide.
    hours = encode_to_led_bits(now.hour, 5, 0x0000FF, 0x202040)
    #Minutes. Deep green for on, pale green for off. Six bits wide.
    mins = encode_to_led_bits(now.minute, 6, 0x00FF00, 0x204020)
    #Seconds. Red for on, pink for off. Six bits wide.
    secs = encode_to_led_bits(now.second, 6, 0xFF0000, 0x402020)

    #Concatenate the time parts together. Puts two turned-off pixels between
    #each.
    time = [0,0] + secs + [0,0] + mins + [0,0] + hours
    #Fill the frame out and then return it.
    return fill_time_frame(time, now.second)

time_colors = {
    0: 0xFF0000,
    1: 0xFFa500,
    2: 0xFFFF00,
    3: 0x00FF00,
    4: 0x0000FF,
    5: 0xFF00FF
}

#Fills the unused remainder of the strip with solid color. Just cycles through
#the rainbow to give a bit of visual appeal.
def fill_time_frame(frame, secs):
    return [time_colors[secs // 10] for i in range(BlinkyTape.LED_COUNT - len(frame))] + frame

blinkyTape = None
try:
    #Create a BlinkyTape client object.
    blinkyTape = BlinkyTape(SERIAL_ADDRESS)
    
    #Initiate the tape's brightness. 10 is a pretty good setting
    #for developing in a dim room without burning your eyes out!
    #Edit this upward to display the clock in brighter-lit areas.
    blinkyTape.setBrightness(10)

    #Main loop. Once a second, get the binary-encoded time and send it to the tape.
    while True:
        blinkyTape.setColors(encode_time())
        sleep(1)
finally:
    if blinkyTape:
        #If the program exits the infinite loop controllably (e.g. by
        #keyboard interrupt exception) politely reset the blinkytape to
        #its initial state.
        blinkyTape.reset()
