import gc
import time 
from machine import Pin, SPI
import gc9a01

gc.enable()
gc.collect()

def main():
    spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
    tft = gc9a01.GC9A01(spi,240,240,reset=Pin(9, Pin.OUT),cs=Pin(13, Pin.OUT),dc=Pin(8, Pin.OUT),backlight=Pin(14, Pin.OUT),rotation=0)
    TFT.init()

    # cycle thru jpg's
    while True:
        for image in ["bigbuckbunny.jpg", "bluemarble.jpg"]:
            tft.jpg(image, 0, 0, gc9a01.SLOW)
            time.sleep(5)


main()
