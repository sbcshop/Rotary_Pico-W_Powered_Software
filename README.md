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
- Pico W and RFID module interfacing
  
  | Pico W | NFC Module Pin | Function |
  |---|---|---|
  |GP4 | RX | Serial UART connection |
  |GP5 | TX  | Serial UART connection |

  
- Pico W and Display interfacing
  
  | Pico W | Display Pin | Function |
  |---|---|---|
  |GP10 | SCLK | Clock pin of SPI interface for display|
  |GP11 | DIN  | MOSI (Master OUT Slave IN) data pin of SPI interface|
  |GP8 | DC | Data/Command pin of SPI interface|
  |GP9 | CS   | Chip Select pin of SPI interface for display|
  |GP12 | Reset | Display Reset Pin |
  
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

