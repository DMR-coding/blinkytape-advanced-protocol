##An OO python client for the frame_protocol_firmware.ino firmware.
##Supports four operations:
##    setColor-- Sets all LEDS to a single color.
##    setColors-- Pass an array of color values to set all LEDs individually.
##    setBrightness-- Set the strip's brightness. (Blinkytape supports 0 through 93)
##    reset-- Turn all the LEDs off and flush the tape-side serial buffer

## Requires third party module "pySerial." Project page: http://pyserial.sourceforge.net/
## Easiest to get it is from PyPi via pip: "pip install pyserial"

import serial

##Numeric indentifiers for the four commands our control protocol knows.
CODE_SET_COLORS = 0x01
CODE_SET_BRIGHTNESS = 0x02
CODE_SET_COLOR = 0x03
CODE_RESET = 0x00

class BlinkyTape:
    LED_COUNT = 60
    #Constructor. Takes a serial URL (e.g. "COM6" or "/dev/ttyUSB0") indicating the
    #serial port where your blinkytape is attached.
    def __init__(self, serialURL):
        self.serial = serial.serial_for_url(serialURL)

    def __del__(self):
        if self.serial:
            self.serial.close()

    #Set all the LEDs of the strip to a single color.
    def setColor(self, color):
        self.serial.write([CODE_SET_COLOR])
        self.serial.write(color.to_bytes(3, "big"))

    #Takes an array of integer values specifying LED states.
    #Think of them as hex color codes: 0xRRGGBB.
    def setColors(self, leds):
        if len(leds) != self.LED_COUNT:
            raise Exception("Wrong number of values passed.")
        self.serial.write([CODE_SET_COLORS])
        for value in leds:
            self.serial.write(value.to_bytes(3, "big"))

    #Set the brightness level of your BlinkyTape. BlinkyTape's brightness values
    #evidently go (rather arbitrarily) from 0 to 93.
    #Note: Blinkytape gets very bright! Something more like 10 is recommended under dim lighting.
    def setBrightness(self, brightness):
        if brightness < 0 or brightness > 93:
            raise Exception("Brightness out of allowable range.")
        self.serial.write([CODE_SET_BRIGHTNESS, brightness])

    #Reset the blinkytape. This causes the tape to set all its LEDs off and
    #flush its serial read buffer.
    def reset(self):
        self.serial.write([CODE_RESET])
