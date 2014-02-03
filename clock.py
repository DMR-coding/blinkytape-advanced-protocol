import serial
from datetime import datetime
from time import sleep

#You'll need to edit this line to match the
#serial address where your blinkytape is actually attached.
SERIAL_ADDRESS = "COM6"
LED_COUNT = 60

def write_solid_frame(color, port):
    port.write([0x03])
    port.write(color.to_bytes(3, "big"))

def write_led_frame(leds, port):
    if len(leds) != LED_COUNT:
        raise Exception("Wrong number of values passed.")
    port.write([0x01])
    for value in leds:
        port.write(value.to_bytes(3, "big"))

def write_brightness_frame(brightness, port):
    if brightness < 0 or brightness > 93:
        raise Exception("Brightness out of allowable range.")
    port.write([0x02, brightness])

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
    return fill_time_fram(time, now.second)

time_colors = {
    0: 0xFF0000,
    1: 0xFFa500,
    2: 0xFFFF00,
    3: 0x00FF00,
    4: 0x0000FF,
    5: 0xFF00FF
}

def fill_time_fram(frame, secs):
    return [time_colors[secs // 10] for i in range(LED_COUNT - len(frame))] + frame

try:
    port = serial.serial_for_url(SERIAL_ADDRESS)
    write_brightness_frame(30, port)
    while True:
        write_led_frame(encode_time(), port)
        sleep(1)
finally:
    write_solid_frame(0x404040, port)
    port.close()
