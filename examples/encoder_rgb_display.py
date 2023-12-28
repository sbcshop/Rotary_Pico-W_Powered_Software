import sys
from RotaryEncoder import Rotary,Rotary_set
from machine import Pin, SPI
import gc9a01
import neopixel
import utime,time
import italicc
import vga1_bold_16x32 as font


np = neopixel.NeoPixel(machine.Pin(15), 32)

spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = gc9a01.GC9A01(spi,240,240,reset=Pin(9, Pin.OUT),cs=Pin(13, Pin.OUT),dc=Pin(8, Pin.OUT),backlight=Pin(14, Pin.OUT),rotation=3)
    
r = Rotary(
              min_val=0,
              max_val=32, 
              reverse=False,
              range_mode=Rotary_set.RANGE_WRAP,
              pull_up=False,
              half_step=True) # change here to full step

val_old = r.value()


def display(): 
    tft.init()
    tft.rotation(0)
    tft.fill(gc9a01.BLACK)
    utime.sleep(0.5)
    tft.text(font, "Rotary", 60, 50, gc9a01.RED)

display()

colors = [(100, 0, 0),(0, 100, 0),(0, 0, 100)]
i = 0
j = 0
while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        np[i] = colors[j] # set to red, full brightness
        np.write()
        print('result =', str(val_new))
        tft.text(font,str(val_new), 100, 150, gc9a01.GREEN)
        time.sleep(0.1)
        tft.text(font,str(val_new), 100, 150, gc9a01.BLACK)
        i += 1
        if i == 32:
            i=0
            j +=1
            if j == 3:
                j = 0

    time.sleep_ms(50)
