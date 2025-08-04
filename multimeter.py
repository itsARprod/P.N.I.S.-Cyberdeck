from machine import Pin, ADC, I2C, PWM
import ssd1306
import utime
import p


mode_names = ["Voltage", "Continuity"]
mode = 0

# Helper to read voltage with calibration
def read_voltage():
    raw = adc_voltage.read_u16()
    v_adc = raw * 3.3 / 65535
    real_voltage = v_adc * 4 * 1.296   # Use same multiplier as your working test
    return round(real_voltage, 2)

def draw_screen(value, unit):
    p.oled.fill(0)
    p.oled.text("Multimeter", 25, 0)
    p.oled.text(f"{value} {unit}", 30, 24)
    p.oled.text(f"Mode: {mode_names[mode]}", 10, 50)
    p.oled.show()

def run_multimeter():
    global adc_pin
    global adc_voltage
    global adc_continuity
        # LED for continuity (GP21)
    led = Pin(21, Pin.OUT)
    led.value(0)

    # ADC input
    adc_pin = Pin(26,mode=Pin.IN)
    adc_voltage = ADC(adc_pin)  # GP26
    adc_continuity = Pin(27, Pin.IN, Pin.PULL_UP)  # GP27 with pull-up

    # Multimeter detection (GP20)
    detect_pin = Pin(20, Pin.IN, Pin.PULL_UP)
    

    global mode
    draw_screen("--", "")

    while True:
        if detect_pin.value() == 1:
            p.oled.fill(0)
            p.oled.text("Please connect", 10, 20)
            p.oled.text("the multimeter", 6, 32)
            p.oled.text("addon!", 40, 44)
            p.oled.show()
        while detect_pin.value() == 1:
            if p.pins[4].value() == 0:
                p.play_tone(500, 0.1)
                return
            utime.sleep(0.1)
        if mode == 0:
            value = read_voltage()
            draw_screen(value, "V")
            led.value(0)
            buzzer.duty_u16(0)

        elif mode == 1:
            if adc_continuity.value() == 0:
                draw_screen("Connected", "")
                led.value(1)
                buzzer.freq(1000)
                buzzer.duty_u16(30000)
            else:
                draw_screen("Open", "")
                led.value(0)
                buzzer.duty_u16(0)

        if p.pins[1].value() == 0:  # RIGHT
            mode = (mode + 1) % len(mode_names)
            p.play_tone(1200, 0.05)
            while p.pins[1].value() == 0:
                pass

        elif p.pins[2].value() == 0:  # LEFT
            mode = (mode - 1) % len(mode_names)
            p.play_tone(800, 0.05)
            while p.pins[2].value() == 0:
                pass

        elif p.pins[4].value() == 0:
            p.play_tone(500, 0.1)
            led.value(0)
            buzzer.duty_u16(0)
            break

        utime.sleep(0.1)

