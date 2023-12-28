from machine import Pin, SPI ,UART
import sdcard
import os
import utime,time
from machine import Pin, UART,SPI


status_led = machine.Pin(25, machine.Pin.OUT)#led_1 connected to pico pin 25
status_led.value(1)


def sdtest(data):
    spi=SPI(0,sck=Pin(18),mosi=Pin(19),miso=Pin(16))
    sd=sdcard.SDCard(spi,Pin(17))
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/fc")
    print("Filesystem check")
    
    print(os.listdir("/fc"))

    fn = "/fc/File.txt"
    print()
    print("Single block read/write")
    with open(fn, "a") as f:
        n = f.write(data)
        print(n, "bytes written") 

    with open(fn, "r") as f:
        result2 = f.read()
        print(len(result2), "bytes read")

    os.umount("/fc")

while True:
    sdtest('Hello World!!! \n')
    utime.sleep(0.5)
