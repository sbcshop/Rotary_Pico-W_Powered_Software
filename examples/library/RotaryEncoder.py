import micropython
from machine import Pin
from machine import Pin,I2C,SPI,PWM,Timer
import framebuf
import time

#Pin definition
I2C_SDA = 6
I2C_SDL = 7

I2C_RST = 4
I2C_INT = 5

IRQ_RISING_FALLING = Pin.IRQ_RISING | Pin.IRQ_FALLING

_DIR_CW = const(0x10)  # Clockwise step
_DIR_CCW = const(0x20)  # Counter-clockwise step

# Rotary Encoder States
_R_START = const(0x0)
_R_CW_1 = const(0x1)
_R_CW_2 = const(0x2)
_R_CW_3 = const(0x3)
_R_CCW_1 = const(0x4)
_R_CCW_2 = const(0x5)
_R_CCW_3 = const(0x6)
_R_ILLEGAL = const(0x7)

_transition_table = [

    # |------------- NEXT STATE -------------|            |CURRENT STATE|
    # CLK/DT    CLK/DT     CLK/DT    CLK/DT
    #   00        01         10        11
    [_R_START, _R_CCW_1, _R_CW_1,  _R_START],             # _R_START
    [_R_CW_2,  _R_START, _R_CW_1,  _R_START],             # _R_CW_1
    [_R_CW_2,  _R_CW_3,  _R_CW_1,  _R_START],             # _R_CW_2
    [_R_CW_2,  _R_CW_3,  _R_START, _R_START | _DIR_CW],   # _R_CW_3
    [_R_CCW_2, _R_CCW_1, _R_START, _R_START],             # _R_CCW_1
    [_R_CCW_2, _R_CCW_1, _R_CCW_3, _R_START],             # _R_CCW_2
    [_R_CCW_2, _R_START, _R_CCW_3, _R_START | _DIR_CCW],  # _R_CCW_3
    [_R_START, _R_START, _R_START, _R_START]]             # _R_ILLEGAL

_transition_table_half_step = [
    [_R_CW_3,            _R_CW_2,  _R_CW_1,  _R_START],
    [_R_CW_3 | _DIR_CCW, _R_START, _R_CW_1,  _R_START],
    [_R_CW_3 | _DIR_CW,  _R_CW_2,  _R_START, _R_START],
    [_R_CW_3,            _R_CCW_2, _R_CCW_1, _R_START],
    [_R_CW_3,            _R_CW_2,  _R_CCW_1, _R_START | _DIR_CW],
    [_R_CW_3,            _R_CCW_2, _R_CW_3,  _R_START | _DIR_CCW],
    [_R_START,           _R_START, _R_START, _R_START],
    [_R_START,           _R_START, _R_START, _R_START]]

_STATE_MASK = const(0x07)
_DIR_MASK = const(0x30)


def _wrap(value, incr, lower_bound, upper_bound):
    range = upper_bound - lower_bound + 1
    value = value + incr

    if value < lower_bound:
        value += range * ((lower_bound - value) // range + 1)

    return lower_bound + (value - lower_bound) % range


def _bound(value, incr, lower_bound, upper_bound):
    return min(upper_bound, max(lower_bound, value + incr))


def _trigger(rotary_instance):
    for listener in rotary_instance._listener:
        listener()


class Rotary(object):

    RANGE_UNBOUNDED = const(1)
    RANGE_WRAP = const(2)
    RANGE_BOUNDED = const(3)

    def __init__(self, min_val, max_val, reverse, range_mode, half_step, invert):
        self._min_val = min_val
        self._max_val = max_val
        self._reverse = -1 if reverse else 1
        self._range_mode = range_mode
        self._value = min_val
        self._state = _R_START
        self._half_step = half_step
        self._invert = invert
        self._listener = []

    def set(self, value=None, min_val=None,
            max_val=None, reverse=None, range_mode=None):
        # disable DT and CLK pin interrupts
        self._hal_disable_irq()

        if value is not None:
            self._value = value
        if min_val is not None:
            self._min_val = min_val
        if max_val is not None:
            self._max_val = max_val
        if reverse is not None:
            self._reverse = -1 if reverse else 1
        if range_mode is not None:
            self._range_mode = range_mode
        self._state = _R_START

        # enable DT and CLK pin interrupts
        self._hal_enable_irq()

    def value(self):
        return self._value

    def reset(self):
        self._value = 0

    def close(self):
        self._hal_close()

    def add_listener(self, l):
        self._listener.append(l)

    def remove_listener(self, l):
        if l not in self._listener:
            raise ValueError('{} is not an installed listener'.format(l))
        self._listener.remove(l)
        
    def _process_rotary_pins(self, pin):
        old_value = self._value
        clk_dt_pins = (self._hal_get_clk_value() <<
                       1) | self._hal_get_dt_value()
                       
        if self._invert:
            clk_dt_pins = ~clk_dt_pins & 0x03
            
        # Determine next state
        if self._half_step:
            self._state = _transition_table_half_step[self._state &
                                                      _STATE_MASK][clk_dt_pins]
        else:
            self._state = _transition_table[self._state &
                                            _STATE_MASK][clk_dt_pins]
        direction = self._state & _DIR_MASK

        incr = 0
        if direction == _DIR_CW:
            incr = 1
        elif direction == _DIR_CCW:
            incr = -1

        incr *= self._reverse

        if self._range_mode == self.RANGE_WRAP:
            self._value = _wrap(
                self._value,
                incr,
                self._min_val,
                self._max_val)
        elif self._range_mode == self.RANGE_BOUNDED:
            self._value = _bound(
                self._value,
                incr,
                self._min_val,
                self._max_val)
        else:
            self._value = self._value + incr

        try:
            if old_value != self._value and len(self._listener) != 0:
                micropython.schedule(_trigger, self)
        except:
            pass
        
class RotaryIRQ(Rotary):
    def __init__(
        self,
        pin_num_clk=2,
        pin_num_dt=3,
        min_val=0,
        max_val=10,
        reverse=False,
        range_mode=Rotary.RANGE_UNBOUNDED,
        pull_up=False,
        half_step=False,
        invert=False,
    ):
        super().__init__(min_val, max_val, reverse, range_mode, half_step, invert)

        if pull_up:
            self._pin_clk = Pin(pin_num_clk, Pin.IN, Pin.PULL_UP)
            self._pin_dt = Pin(pin_num_dt, Pin.IN, Pin.PULL_UP)
        else:
            self._pin_clk = Pin(pin_num_clk, Pin.IN)
            self._pin_dt = Pin(pin_num_dt, Pin.IN)

        self._hal_enable_irq()

    def _enable_clk_irq(self):
        self._pin_clk.irq(self._process_rotary_pins, IRQ_RISING_FALLING)

    def _enable_dt_irq(self):
        self._pin_dt.irq(self._process_rotary_pins, IRQ_RISING_FALLING)

    def _disable_clk_irq(self):
        self._pin_clk.irq(None, 0)

    def _disable_dt_irq(self):
        self._pin_dt.irq(None, 0)

    def _hal_get_clk_value(self):
        return self._pin_clk.value()

    def _hal_get_dt_value(self):
        return self._pin_dt.value()

    def _hal_enable_irq(self):
        self._enable_clk_irq()
        self._enable_dt_irq()

    def _hal_disable_irq(self):
        self._disable_clk_irq()
        self._disable_dt_irq()

    def _hal_close(self):
        self._hal_disable_irq()


#Touch driver
class Touch_CST816T(object):
    #Initialize the touch chip  
    def __init__(self,address=0x15,mode=0,i2c_num=1,i2c_sda=6,i2c_scl=7,int_pin=5,rst_pin=4):
        self._bus = I2C(id=i2c_num,scl=Pin(i2c_scl),sda=Pin(i2c_sda),freq=400_000) # Initialize I2C
        self._address = address #Set slave address
        self.int=Pin(int_pin,Pin.IN, Pin.PULL_UP)
        self.tim = Timer()     
        self.rst=Pin(rst_pin,Pin.OUT)
        self.Reset()
        

        self.Mode = mode
        self.Gestures="None"
        self.Flag = self.Flgh =self.l = 0
        self.X_point = self.Y_point = 0
        self.int.irq(handler=self.Int_Callback,trigger=Pin.IRQ_FALLING)

    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
    
    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
    
    def _write_byte(self,cmd,val):
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))

    def WhoAmI(self):
        if (0xB5) != self._read_byte(0xA7):
            return False
        return True
    
    def Read_Revision(self):
        return self._read_byte(0xA9)
      
    #Stop sleeping  
    def Stop_Sleep(self):
        self._write_byte(0xFE,0x01)
    
    #Reset 
    def Reset(self):
        self.rst(0)
        time.sleep_ms(1)
        self.rst(1)
        time.sleep_ms(50)
    
    #Set mode  
    def Set_Mode(self,mode,callback_time=10,rest_time=5): 
        # mode = 0 gestures mode 
        # mode = 1 point mode 
        # mode = 2 mixed mode
        
        if (mode == 1):      
            self._write_byte(0xFA,0X41)
            print("m0")
            
        elif (mode == 2) :
            self._write_byte(0xFA,0X71)
            print("m2")
            
        else:
            self._write_byte(0xFA,0X11)
            self._write_byte(0xEC,0X01)
            
    #Get the coordinates of the touch  
    def get_point(self):
        xy_point = self._read_block(0x03,4)
        
        x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
        y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]
        
        self.X_point=x_point
        self.Y_point=y_point
        #print("x = ",self.X_point)
        #print("y = ",self.Y_point)
        return [self.X_point,self.Y_point]
    
    #Gesture  
    def Touch_Gesture(self):
        self.Mode = 0
        self.Set_Mode(self.Mode)

        time.sleep(1)
        print(self.Gestures)

        while self.Gestures != 0x01:
            print("UP")
            time.sleep(0.2)
            
        while self.Gestures != 0x02:
            print("DOWM")
            time.sleep(0.2)
            
        while self.Gestures != 0x03:
            print("LEFT")
            time.sleep(0.2)
            
        while self.Gestures != 0x04:
            print("RIGHT")
            time.sleep(0.2)
            
        while self.Gestures != 0x0C:
            print("Long Press")
            time.sleep(0.2)
            
        while self.Gestures != 0x0B:
            print("Double Click")
            time.sleep(0.2)
 
        
    def Int_Callback(self,pin):
        if self.Mode == 0 :
            self.Gestures = self._read_byte(0x01)

        elif self.Mode == 1:           
            self.Flag = 1
            self.get_point()

    def Timer_callback(self,t):
        self.l += 1
        if self.l > 100:
            self.l = 50

