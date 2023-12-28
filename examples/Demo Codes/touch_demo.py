from RotaryEncoder import Touch
import time

touch=Touch(mode=0)

while 1:
    d = touch.get_point()
    touch.Reset()
    print(d)
    time.sleep(0.2)
    
