import serial

class BlinkyTape:
    LED_COUNT = 60
    def __init__(self, serialURL):
        self.serial = serial.serial_for_url(serialURL)

    def __del__(self):
        if self.serial:
            self.serial.close()

    def setColor(self, color):
        self.serial.write([0x03])
        self.serial.write(color.to_bytes(3, "big"))

    def setColors(self, leds):
        if len(leds) != self.LED_COUNT:
            raise Exception("Wrong number of values passed.")
        self.serial.write([0x01])
        for value in leds:
            self.serial.write(value.to_bytes(3, "big"))

    def setBrightness(self, brightness):
        if brightness < 0 or brightness > 93:
            raise Exception("Brightness out of allowable range.")
        self.serial.write([0x02, brightness])
