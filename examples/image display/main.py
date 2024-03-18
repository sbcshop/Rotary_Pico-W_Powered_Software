'''
Save images into Pico W of Rotary:
https://github.com/sbcshop/Rotary_Pico-W_Powered_Software/tree/main/examples/image%20display

'''
import gc
import time 
from machine import Pin, SPI
import gc9a01

gc.enable()
gc.collect()

spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = gc9a01.GC9A01(spi,240,240,reset=Pin(9, Pin.OUT),cs=Pin(13, Pin.OUT),dc=Pin(8, Pin.OUT),backlight=Pin(14, Pin.OUT),rotation=0)
tft.init()

# cycle thru jpg's
while True:
    for image in ["shinchan.jpg", "tiger.jpg","nature.jpg", "bluemarble.jpg"]:
        tft.jpg(image, 0, 0, gc9a01.SLOW)
        time.sleep(2)
