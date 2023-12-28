from machine import Pin, SPI
import time
import gc9a01
import utime
import italicc
import vga1_bold_16x32 as font
#import vga1_bold_16x16 as font


spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = gc9a01.GC9A01(spi,240,240,reset=Pin(9, Pin.OUT),cs=Pin(13, Pin.OUT),dc=Pin(8, Pin.OUT),backlight=Pin(14, Pin.OUT),rotation=3)
    

tft.init()
tft.rotation(0)
tft.fill(gc9a01.BLACK)
utime.sleep(0.5)
tft.text(font, "ROTARY", 60, 50, gc9a01.WHITE,gc9a01.BLACK)
tft.text(font, "HELLO WORLD", 30, 100, gc9a01.GREEN,gc9a01.BLACK)
