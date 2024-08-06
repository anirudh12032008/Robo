import time
from machine import Pin, PWM,I2C
from ssd1306 import SSD1306_I2C

# Define buzzer pin
BUZZER_PIN = 15
buzzer = PWM(Pin(BUZZER_PIN))


# Define keypad
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


# screen
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
oled.text("Hiiiii", 0,0)
oled.show()

def get_key():
    for r in range(ROWS):
        row_pins[r].value(1)
        for c in range(COLS):
            if col_pins[c].value():
                while col_pins[c].value():
                    pass  # Wait until key is released
                row_pins[r].value(0)
                return keys[r][c]
        row_pins[r].value(0)
    return None  # No key pressed

def buzz():
    buzzer.freq(1000)  # Frequency in Hz
    buzzer.duty_u16(32768)  # Adjust the duty cycle for volume (50% in this case)
    time.sleep(0.1)
    buzzer.duty_u16(0)  # Turn off buzzer

# Main loop
while True:
    key = get_key()
    if key is not None:
        print(f"Key pressed: {key}")  
        oled.text(f"Key pressed: {key}", 0,0)
        oled.show()
        # Print the key pressed to the console
        buzz()  # Sound buzzer when key is pressed
    time.sleep(0.1)
