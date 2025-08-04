from machine import Pin, PWM, I2C
import utime
import ssd1306

# I2C OLED setup (128x64, GP0 = SDA, GP1 = SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Define input pins for 5 buttons (GP2–GP6)
pins = [Pin(i, Pin.IN, Pin.PULL_UP) for i in range(2, 7)]

# Set up PWM on GP7 for buzzer
buzzer = PWM(Pin(7))
buzzer.duty_u16(0)

def play_tone(freq, duration):
    buzzer.freq(freq)
    buzzer.duty_u16(32768)
    utime.sleep(duration)
    buzzer.duty_u16(0)
    
def wait_for_release(pin):
    while pin.value() == 0:
        utime.sleep(0.01)
        
