from machine import Pin, SPI
import italicc
import vga1_bold_16x32 as font
import urequests
import network
import gc9a01
import time,utime
import romancs

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Tech SB_2G","jc643111h@")# SSID and Password of wifi here
openweather_api_key = "dff350f24230806454d5f48aebbf97bb"



spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = gc9a01.GC9A01(spi,240,240,reset=Pin(9, Pin.OUT),cs=Pin(13, Pin.OUT),dc=Pin(8, Pin.OUT),backlight=Pin(14, Pin.OUT),rotation=0)

def cycle(p):
    try:
        len(p)
    except TypeError:
        cache = []
        for i in p:
            yield i
            cache.append(i)
        p = cache
    while p:
        yield from p
        
###################################
colors = cycle([0xe000, 0xece0, 0xe7e0, 0x5e0, 0x00d3, 0x7030])
foreground = next(colors)
background = gc9a01.BLACK

tft.init()
tft.fill(background)
utime.sleep(1)

height = tft.height()
width = tft.width()
last_line = width - font.HEIGHT

tfa = 0        # top free area
tfb = 0        # bottom free area
tft.vscrdef(tfa, height, tfb)

scroll = 0
character = font.FIRST
###################################

def display(): 
    tft.init()
    tft.rotation(0)
    tft.fill(gc9a01.BLACK)
    time.sleep(0.1)
    tft.text(font, "Weather", 60, 10, gc9a01.RED)

display()

# connect the network       
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
 
# syncing the time
import ntptime
while True:
    try:
        ntptime.settime()
        print('Time Set Successfully')
        break
    except OSError:
        print('Time Setting...')
        continue
 

string = 'Loading...'
 
 
# Open Weather
TEMPERATURE_UNITS = {
    "standard": "K",
    "metric": "°C",
    "imperial": "°F",
}
 
SPEED_UNITS = {
    "standard": "m/s",
    "metric": "m/s",
    "imperial": "mph",
}
 
units = "metric"
 
def get_weather(city, api_key, units='metric', lang='en'):
    '''
    Get weather data from openweathermap.org
        city: City name, state code and country code divided by comma, Please, refer to ISO 3166 for the state codes or country codes. https://www.iso.org/obp/ui/#search
        api_key: Your unique API key (you can always find it on your openweather account page under the "API key" tab https://home.openweathermap.org/api_keys
        unit: Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default. More: https://openweathermap.org/current#data
        lang: You can use this parameter to get the output in your language. More: https://openweathermap.org/current#multi
    '''
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}&lang={lang}"
    #print(url)
    res = urequests.post(url)
    return res.json()
 
def print_weather(weather_data):
    print(f'Timezone: {int(weather_data["timezone"] / 3600)}')
    sunrise = time.localtime(weather_data['sys']['sunrise']+weather_data["timezone"])
    sunset = time.localtime(weather_data['sys']['sunset']+weather_data["timezone"])
    print(f'Sunrise: {sunrise[3]}:{sunrise[4]}')
    print(f'Sunset: {sunset[3]}:{sunset[4]}')   
    print(f'Country: {weather_data["sys"]["country"]}')
    print(f'City: {weather_data["name"]}')
    print(f'Coordination: [{weather_data["coord"]["lon"]}, {weather_data["coord"]["lat"]}')
    print(f'Visibility: {weather_data["visibility"]}m')
    print(f'Weather: {weather_data["weather"][0]["main"]}')
    print(f'Temperature: {weather_data["main"]["temp"]}{TEMPERATURE_UNITS[units]}')
    print(f'Temperature min: {weather_data["main"]["temp_min"]}{TEMPERATURE_UNITS[units]}')
    print(f'Temperature max: {weather_data["main"]["temp_max"]}{TEMPERATURE_UNITS[units]}')
    print(f'Temperature feels like: {weather_data["main"]["feels_like"]}{TEMPERATURE_UNITS[units]}')
    print(f'Humidity: {weather_data["main"]["humidity"]}%')
    print(f'Pressure: {weather_data["main"]["pressure"]}hPa')
    print(f'Wind speed: {weather_data["wind"]["speed"]}{SPEED_UNITS[units]}')
    #print(f'Wind gust: {weather_data["wind"]["gust"]}{SPEED_UNITS[units]}')
    print(f'Wind direction: {weather_data["wind"]["deg"]}°')
    if "clouds" in weather_data:
        print(f'Cloudiness: {weather_data["clouds"]["all"]}%')
    elif "rain" in weather_data:
        print(f'Rain volume in 1 hour: {weather_data["rain"]["1h"]}mm')
        print(f'Rain volume in 3 hour: {weather_data["rain"]["3h"]}mm')
    elif "snow" in weather_data:
        print(f'Snow volume in 1 hour: {weather_data["snow"]["1h"]}mm')
        print(f'Snow volume in 3 hour: {weather_data["snow"]["3h"]}mm')
    
    tft.text(font,f'Temp:{weather_data["main"]["temp"]}{TEMPERATURE_UNITS[units]}', 20, 50, gc9a01.WHITE)
    tft.text(font,f'Humi:{weather_data["main"]["humidity"]}%', 20, 85, gc9a01.WHITE)
    tft.text(font,f'Pres:{weather_data["main"]["pressure"]}hPa', 20, 115, gc9a01.WHITE)
    tft.text(font,f'Wind:{weather_data["wind"]["speed"]}{SPEED_UNITS[units]}', 20, 145, gc9a01.WHITE)
    tft.text(font,f'Visi:{weather_data["visibility"]}m', 20, 175, gc9a01.WHITE)
    
 
 
while True:
        # get weather
        if scroll % font.HEIGHT == 0:
            line = (scroll + last_line) % height
            
            weather_data = get_weather('london', openweather_api_key, units=units)
            weather=weather_data["weather"][0]["main"]
            t=weather_data["main"]["temp"]
            rh=weather_data["main"]["humidity"]
         
            # get time
            hours=time.localtime()[3]+int(weather_data["timezone"] / 3600)
            mins=time.localtime()[4]
         
            string = f'{hours:02d}:{mins:02d} {weather}\n'
            string = f'{t}{TEMPERATURE_UNITS[units]} {rh}%rh'
         
            # shell print
            print_weather(weather_data)
         
            # refresh every 10s
            #time.sleep(0.001)
            
            # change color for next line
            foreground = next(colors)

            # next character with rollover at 256
            character += 1
            if character > font.LAST:
                character = font.FIRST

        # scroll the screen up 1 row
        tft.vscsad(scroll+tfa)
        scroll += 1
        scroll %= height

        utime.sleep(0.03)
