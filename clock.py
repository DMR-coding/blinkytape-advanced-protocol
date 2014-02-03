import sys
sys.path.append("./frame_protocol")
from BlinkyTape import BlinkyTape
from datetime import datetime
from time import sleep

#You'll need to edit this line to match the
#serial address where your blinkytape is actually attached.
SERIAL_ADDRESS = "COM6"

def encode_to_led_bits(num, numBits, onColor, offColor):
    byts = []
    for i in [2**n for n in range(numBits)]:
        if num & i == 0:
            byts.append(offColor)
        else:
            byts.append(onColor)
    return byts

def encode_time():
    now = datetime.now()
    hours = encode_to_led_bits(now.hour, 5, 0x0000FF, 0x202040)
    mins = encode_to_led_bits(now.minute, 6, 0x00FF00, 0x204020)
    secs = encode_to_led_bits(now.second, 6, 0xFF0000, 0x402020)

    time = [0,0] + secs + [0,0] + mins + [0,0] + hours
    return fill_time_frame(time, now.second)

time_colors = {
    0: 0xFF0000,
    1: 0xFFa500,
    2: 0xFFFF00,
    3: 0x00FF00,
    4: 0x0000FF,
    5: 0xFF00FF
}

def fill_time_frame(frame, secs):
    return [time_colors[secs // 10] for i in range(BlinkyTape.LED_COUNT - len(frame))] + frame

blinkyTape = None
try:
    blinkyTape = BlinkyTape(SERIAL_ADDRESS)
    blinkyTape.setBrightness(30)
    while True:
        blinkyTape.setColors(encode_time())
        sleep(1)
finally:
    if blinkyTape:
        blinkyTape.setColor(0x404040)
