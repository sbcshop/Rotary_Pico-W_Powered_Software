# Rotary_Pico-W_Powered_Software

<img src = "https://github.com/sbcshop/Rotary_Pico-W_Powered_Software/blob/main/images/img1.png">

#### "Dive into innovation with our Rotary Encoder – boasting 32 vibrant RGB LED arrays, an intuitive turning knob, and a dazzling 1.28" Round Touch LCD. Unleash your creativity with a seamless user interface, powered by the brilliance of LVGL, the go-to free and open-source embedded graphics library. Craft personalized and stunning UIs effortlessly for any MCU, MPU, and display type, giving you boundless design freedom. Your Rotary, your style – customize the interface to match your unique vision and make a statement in the world of limitless possibilities."

This GitHub page offers a step-by-step tutorial for using Rotary Pico W. 

### Features : 
- Device powered by powerful Pico W which has a Dual-core Arm Cortex M0+ processor, a flexible clock running up to 133 MHz
- Inbuilt Wi-Fi & Bluetooth LE for wireless connectivity
- It has 264kB of SRAM and 2MB of on-board flash memory
- It has a Rotary encoder
- 1.28" TFT display with a resolution of 240 x 240 pixels for visual interactions
- Round display has capacitive touch
- GPIO having Crocodile clip connector for interfacing additional peripherals 
- It has an onboard SD Card
- On board 32 RGB (WS2812B) Led's


### Interfacing Details
- Pico W and Touch interfacing
  
  | Pico W | NFC Module Pin | Function |
  |---|---|---|
  |GP6 | SDA | Touch I2C  |
  |GP7 | SCL  | Touch I2C  |
  |GP4 | RESET  | Touch Reset  |
  |GP7 | INT  | Touch Intrrupt  |

  
- Pico W and Round Display interfacing
  
  | Pico W | Display Pin | Function |
  |---|---|---|
  |GP10 | SCLK  | Clock pin of SPI interface for display|
  |GP11 | DIN   | MOSI (Master OUT Slave IN) data pin of SPI interface|
  |GP12 | DOUT   | MISO (Master OUT Slave OUT) data pin of SPI interface|
  |GP8  | DC    | Data/Command pin of SPI interface|
  |GP13 | CS    | Chip Select pin of SPI interface for display|
  |GP9  | Reset | Display Reset Pin |
  |GP14 | BL    | Display backlight Pin |
  
- Pico W and micro SD card interfacing

  | Pico W | microSD Card | Function |
  |---|---|---|
  |GP18 | SCLK |Clock pin of SPI interface for microSD card |
  |GP19 | DIN  | MOSI (Master OUT Slave IN) data pin of SPI interface|
  |GP16 | DOUT | MISO (Master IN Slave OUT) data pin of SPI interface|
  |GP17 | CS   | Chip Select pin of SPI interface for SDcard|

- RGB LED Interfacing with Pico W
  | Pico W | Buttons | Function |
  |---|---|---|
  |GP15 | RGB LED | OnBoard LED pin of Pico W  |
 
- Breakout GPIOs
  | Pico W |Physical Pin | Multi-Function |
  |---|---|---|
  |GP0 | 1  | General IO / SPI0 RX / I2C0 SDA / UART0 TX /PWM0A |
  |GP1 | 2 | General IO / SPI0 CSn / I2C0 SCL / UART0 RX /PWM0B |
  |GP20 | 26 | General IO / I2C0 SDA0 / PMM2A|
  |GP21 | 27 | General IO / I2C0 SCL0 / PWM2B |
  |GP22 | 29 | General IO / PWM3A |
  |GP26 | 31 | General IO / ADC0 / I2C1 SDA1 / PWM5A |
  |GP27| 32 | General IO / ADC1 / I2C1 SCL1 / PWM5B |



### 1. Step to install boot Firmware
   - Every ReadPi board will be provided with boot firmware already installed, so you can skip this step and directly go to step 2.
   - If in case you want to install firmware for your board, Push and hold the BOOTSEL button and plug your Pico W into the USB port of your computer. Release the BOOTSEL button after your Pico is connected.
   <img src="https://github.com/sbcshop/ArdiPi_Software/blob/main/images/pico_bootmode.gif">
   
   - It will mount as a Mass Storage Device called RPI-RP2.
   - Drag and drop the MicroPython UF2 - [Rotary Pico W_firmware](https://github.com/sbcshop/Rotary_Pico-W_Powered_Software/blob/main/firmware.uf2) file provided in this github onto the RPI-RP2 volume. Your Pico will reboot. You are now running MicroPython on ArdiPi.

### 2. Onboard LED Blink 
   - Download **Thonny IDE** from [Download link](https://thonny.org/) as per your OS and install it.
   - Once done start **Thonny IDE application**, Connect ReadPi to laptop/PC.
   - Select device at the bottom right with a suitable COM port, as shown in the below figure. You might get a different COM port.
     
      <img src= "https://github.com/sbcshop/EnkPi_2.9_Software/blob/main/images/img1.jpg" />
      <img src= "https://github.com/sbcshop/EnkPi_2.9_Software/blob/main/images/img2.jpg" />
      
   - Write simple onboard blink Python code or [Download Led blink code](https://github.com/sbcshop/ReadPi_NFC_Software/blob/main/examples/onboard_ledBlink.py), then click on the green run button to make your script run on ReadPi.
     
      <img src= "https://github.com/sbcshop/EnkPi_2.9_Software/blob/main/images/img3.jpg" />
     
     Now that we've reached this point, you're executing your script through Thonny IDE, so if you unplug Pico, it will stop running. To run your script without using an IDE, simply power up ArdiPi and it should run your script, go to step 3. Once you have transferred your code to the ArdiPi board, to see your script running, just plug in power either way using micro USB or via Vin, both will work.

