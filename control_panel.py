from machine import Pin, I2C, PWM
import ssd1306
import utime
import p
# Pins to toggle
pin_numbers = [20, 21, 22, 26, 27, 28]

selected = 0

def draw():
    global pin_states
    p.oled.fill(0)
    p.oled.text("B-Toggle", 0, 0)
    x_start = 0
    for i, n in enumerate(pin_numbers):
        x = 4 + i * 20
        p.oled.text(f"{n}", x, 24, 1)
        val = str(pin_states[i])
        if i == selected:
            p.oled.fill_rect(x - 2, 30, 16, 10, 1)
            p.oled.text(val, x, 30, 0)
        else:
            p.oled.text(val, x, 30, 1)
    p.oled.show()

def run_control_panel():
    global selected
    global pin_states
    p.pins_out = [Pin(n, Pin.OUT) for n in pin_numbers]
    pin_states = [0] * len(p.pins_out)
    draw()
    while True:
        if p.pins[0].value() == 0:  # U
            pin_states[selected] = 1 - pin_states[selected]
            p.pins_out[selected].value(pin_states[selected])
            p.play_tone(1000, 0.05)
            draw()
            p.wait_for_release(p.pins[0])
            
        elif p.pins[1].value() == 0:  # L
            selected = (selected + 1) % len(p.pins_out)
            p.play_tone(1200, 0.05)
            draw()
            p.wait_for_release(p.pins[1])

        elif p.pins[2].value() == 0:  # R
            selected = (selected - 1) % len(p.pins_out)
            p.play_tone(600, 0.05)
            draw()
            p.wait_for_release(p.pins[2])

        elif p.pins[4].value() == 0:
            p.play_tone(500, 0.1)
            break

        utime.sleep(0.01)

