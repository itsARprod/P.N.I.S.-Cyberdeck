from machine import Pin, I2C, ADC, PWM
import ssd1306
import utime
import urandom
import dice_icons
import p
from framebuf import FrameBuffer, MONO_HLSB

dice_list = [2, 3, 4, 5, 6, 8, 10, 12, 20]

def draw_dice_screen(current_value, pile):
    
    p.oled.fill(0)
    p.oled.text("Y-Add, B-Roll", 0, 0)
    dbuf = FrameBuffer(dice_icons.dice_icons[dice_list[current_value]], 32, 32, MONO_HLSB)
    p.oled.blit(dbuf, 48, 16)
    p.oled.text(",".join(str(v) for v in pile[-5:]), 0, 56)  # Bottom row
    # Left arrow
    p.oled.line(4, 32, 12, 24, 1)
    p.oled.line(4, 32, 12, 40, 1)
    p.oled.line(12, 24, 12, 40, 1)

    # Right arrow
    p.oled.line(124, 32, 116, 24, 1)
    p.oled.line(124, 32, 116, 40, 1)
    p.oled.line(116, 24, 116, 40, 1)
    p.oled.show()
    

def run_dice_roller():
    selected_dice = 6
    dice_pile = []
    draw_dice_screen(selected_dice, dice_pile)

    while True:
        if p.pins[1].value() == 0:  # RIGHT: increase dice value
            selected_dice = (selected_dice + 1) % len(dice_list)
            p.play_tone(1000, 0.05)
            draw_dice_screen(selected_dice, dice_pile)
            p.wait_for_release(p.pins[1])

        elif p.pins[2].value() == 0:  # LEFT: decrease dice value
            selected_dice = (selected_dice - 1) % len(dice_list)
            p.play_tone(800, 0.05)
            draw_dice_screen(selected_dice, dice_pile)
            p.wait_for_release(p.pins[2])

        elif p.pins[3].value() == 0:  # DOWN: add dice to pile
            if len(dice_pile) == 5:
                dice_pile = []
                p.play_tone(400, 0.05)
            else:
                dice_pile.append(dice_list[selected_dice])
                p.play_tone(1200, 0.05)
            draw_dice_screen(selected_dice, dice_pile)
            p.wait_for_release(p.pins[3])

        elif p.pins[0].value() == 0:  # UP: roll all dice
            results = [urandom.getrandbits(8) % die + 1 for die in dice_pile]
            total = sum(results)
            p.oled.fill(0)
            p.oled.text("Results:", 0, 0)
            p.oled.text(",".join(map(str, results)), 0, 20)
            p.oled.text("Total: " + str(total), 0, 45)
            p.oled.show()
            p.play_tone(800, 0.05)
            p.play_tone(1200, 0.05)
            p.wait_for_release(p.pins[0])

        elif p.pins[4].value() == 0:
            p.play_tone(400, 0.1)
            break

        utime.sleep(0.1)

