import time
from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from pico_dht_22 import PicoDHT22


BUZZER_PIN = 15
buzzer = PWM(Pin(BUZZER_PIN))

SERVO1_PIN = 14
SERVO2_PIN = 16
servo1 = PWM(Pin(SERVO1_PIN))
servo2 = PWM(Pin(SERVO2_PIN))

servo1.freq(50)
servo2.freq(50)

ROWS = 4
COLS = 4
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

row_pins = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]
col_pins = [Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN), Pin(12, Pin.IN, Pin.PULL_DOWN), Pin(13, Pin.IN, Pin.PULL_DOWN)]

TRIG_PIN = 2
ECHO_PIN = 3

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
oled.text("Hello Anirudh", 0, 0)
oled.show()

dht_sensor=PicoDHT22(Pin(28,Pin.IN,Pin.PULL_UP),dht11=False)

MIN_DUTY = 1802
MAX_DUTY = 7864

def angle_to_duty(angle):
    return int(MIN_DUTY + (angle / 180) * (MAX_DUTY - MIN_DUTY))

def set_servo_angle(servo, angle):
    if 0 <= angle <= 180:
        duty = angle_to_duty(angle)
        servo.duty_u16(duty)
        print(f"{servo} - {angle} degrees")

def measure_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    while echo.value() == 0:
        pulse_start = time.ticks_us()
    while echo.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distance = pulse_duration * 0.0343 / 2
    return distance

def get_key():
    for r in range(ROWS):
        row_pins[r].value(1)
        for c in range(COLS):
            if col_pins[c].value():
                while col_pins[c].value():
                    pass
                row_pins[r].value(0)
                return keys[r][c]
        row_pins[r].value(0)
    return None

def buzz():
    buzzer.freq(1000)
    buzzer.duty_u16(32768)
    time.sleep(0.1)
    buzzer.duty_u16(0)

time.sleep(1)

while True:
    distance = measure_distance()
    T,H = dht_sensor.read()
    if T is None:
        continue
        print(" sensor error")
    else:
        print("{}'C  {}%".format(T,H))
        oled.text(str('H: ' +"{:0.2f}".format(H)+ "  %",2),0,20)
        oled.text(str('T: ' +"{:0.2f}".format(T)+ "  C",2),0,30)
        oled.show()
    key = get_key()
    if key is not None:
        print(f"Key pressed: {key}")
        oled.text(f"Key pressed: {key}", 0, 40)
        oled.show()
        if key == '1':
            set_servo_angle(servo1,60)
            set_servo_angle(servo2,60)
            time.sleep(2)
        elif key == '2':
            set_servo_angle(servo1,180)
            set_servo_angle(servo2,180)
        elif key == '3':
            set_servo_angle(servo1,90)
            set_servo_angle(servo2,90)
        buzz()
    oled.text("Distance: {:.2f} cm".format(distance), 0, 10)
    oled.show()
    time.sleep(0.1)
