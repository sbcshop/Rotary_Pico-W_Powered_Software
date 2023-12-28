from RotaryEncoder import Rotary,Rotary_set
import utime,time

r = Rotary(
            min_val=0,
            max_val=32, 
            reverse=False,
            range_mode=Rotary_set.RANGE_WRAP,
            pull_up=False,
            half_step=True) # change here to full step

val_old = r.value()

while True:
    val_new = r.value()
    if val_old != val_new:
        val_old = val_new
        print('result =', str(val_new))
    time.sleep_ms(50)
