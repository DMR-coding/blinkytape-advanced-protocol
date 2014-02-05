/* Firmware that implements a simple fixed-frame serial communications protocol
   Frame type is determined by the leading byte:
   0x00: Reset. No body.
   0x01: LED settings array. Body length: 3 * LED_COUNT bytes
   0x02: Set brightess. Body length: 1 byte.
   0x03: Set all LEDs to solid color. Body length: 3 bytes.
   0x04: Set LED at provided index to color. Body length: 1 index byte + 3 RGB bytes
   
   Since USB is assumed to be a generally reliable channel, we just take in commands
   "fire and forget style." However, in the event that a frame IS interrupted, the read
   operation will timeout after IO_TIMEOUT ms and reset the firmware.
*/

#include <FastSPI_LED2.h>

#define LED_COUNT 60 // BlinkyTape has 60 LEDs!
struct CRGB leds[LED_COUNT]; // this struct contains 60 CRGB values.  This is where 

#ifdef REVB // RevB boards have a slightly different pinout.

#define LED_OUT      5
#define BUTTON_IN    13
#define ANALOG_INPUT A11
#define IO_A         15

#else

#define LED_OUT      13
#define BUTTON_IN    10
#define ANALOG_INPUT A9
#define IO_A         7
#define IO_B         11

#endif

#define IO_TIMEOUT 50
#define BAUD_RATE 115200 //Based on BlinkinLabs example code... Not sure of actual capabilities

int count = LED_COUNT;

// first, let's get ready to blink using some FastSPI_LED2 routines
// take a look at the FastSPI_LED2 example called Fast2Dev for more usage info
void setup()
{  
  LEDS.addLeds<WS2811, LED_OUT, GRB>(leds, LED_COUNT); // this configures the BlinkyBoard - leave as is.
  Serial.begin(BAUD_RATE);
  reset();
}

//Reads LED_COUNT RGB byte triplets from the serial port as they
//come available. When the last one is read in, updates the strip.
void read_led_frame(){
  unsigned long lastRead = millis();
  for (int i = 0; i < LED_COUNT; /*no incrementor*/){
      if(Serial.available() >= 3){
          leds[i] = CRGB(Serial.read(), Serial.read(), Serial.read());
          lastRead = millis();
          i++;//Increment control variable
      }else if(millis() - lastRead > IO_TIMEOUT){
        //We've waited much too long for this frame. Presumably, it's been interrupted.
        reset();
        return; 
      }
      
      //else, the loop just reruns with the same value of i.
    }

   LEDS.show();
}

void read_brightness_frame(){
  unsigned long lastRead = millis();
  while (!Serial.available()){
      if(millis() - lastRead > IO_TIMEOUT){
          //We've waited much too long for this frame. Presumably, it's been interrupted.
          reset();
          return; 
        }
  }
      
  LEDS.setBrightness(Serial.read());
  LEDS.show();
}

void read_solid_frame(){
  unsigned long lastRead = millis();
  while (Serial.available() < 3){
      if(millis() - lastRead > IO_TIMEOUT){
          //We've waited much too long for this frame. Presumably, it's been interrupted.
          reset();
          return; 
        }
  }

  show_solid(CRGB(Serial.read(), Serial.read(), Serial.read()));
}

void read_indexed_frame(){
  unsigned long lastRead = millis();
  while (Serial.available() < 4){
      if(millis() - lastRead > IO_TIMEOUT){
          //We've waited much too long for this frame. Presumably, it's been interrupted.
          reset();
          return; 
        }
  }
  
  int index = Serial.read();
  if(index < 0 || index >= LED_COUNT){
     //Index out of bounds!
     reset();
     return; 
  }
  leds[index] = CRGB(Serial.read(), Serial.read(), Serial.read());
  LEDS.show();
}

//This firmware doesn't use LEDS.showColor to avoid the following problem:
// 1) set up pattern in leds, show()
// 2) setColor
// 3) Perform an unrelated operation like brightness
// 4) show() again-- old frame from #1 reappears because leds is still loaded with it.
void show_solid(CRGB color){
    for(int i = 0; i < LED_COUNT; i++){
      leds[i] = color;      
    }
    LEDS.show();
}

void read_frame(){
   switch(Serial.read()){
      case 0x00:
        reset();
        break;
      case 0x01:
        read_led_frame();
        break;
      case 0x02:
        read_brightness_frame();
        break;
      case 0x03:
        read_solid_frame();
        break;
      case 0x04:
        read_indexed_frame();
        break;
      default:
       reset();
       break; 
   }
}

void reset(){
   //turn all the LEDs off
   show_solid(CRGB(0,0,0));

   //Consume and discard the remainder of the serial buffer.
   while(Serial.available()){
     Serial.read();
   }
}

void loop() {
  if ( Serial.available()) {
      read_frame(); 
  }
  
  //Don't spin at top speed if there's nothing available.
  delay(100);
}
