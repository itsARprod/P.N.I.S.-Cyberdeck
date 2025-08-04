from machine import Pin, PWM, I2C
import utime
import ssd1306
import snake_game
import calculator
import multimeter
import control_panel
import dice
import icons
import car
import p
from framebuf import FrameBuffer, MONO_HLSB
# Menu state
option = 0
options = ['Calculator', 'Control Panel', 'Multimeter', 'Dice Roller', 'Snake', 'Car']
sos_hold = 0
apps = {
#snake
'Snake':snake_game.run_snake,
# calculator
'Calculator':calculator.run_calculator,
#control panel
'Control Panel':control_panel.run_control_panel,
#multimeter
'Multimeter':multimeter.run_multimeter,
#dice
'Dice Roller':dice.run_dice_roller,
#car
'Car':car.run_car
}

def draw_menu(opt):
    p.oled.fill(0)
    p.oled.text("B-Confirm", 0, 0)
    # Draw main icon
    '''
    if opt == 0:
        fbuf = FrameBuffer(icons.icon_calculator, 32, 32, MONO_HLSB)
    elif opt == 1:
        fbuf = FrameBuffer(icons.icon_control_panel, 32, 32, MONO_HLSB)
    elif opt == 2:
        fbuf = FrameBuffer(icons.icon_multimeter, 32, 32, MONO_HLSB)
    elif opt == 3:
        fbuf = FrameBuffer(icons.icon_dice, 32, 32, MONO_HLSB)
    elif opt == 4:
        fbuf = FrameBuffer(icons.icon_snake, 32, 32, MONO_HLSB)
    elif opt == 5:
        fbuf = FrameBuffer(icons.icon_car, 32, 32, MONO_HLSB)
    else:
        fbuf = FrameBuffer(icons.icon_missing, 32, 32, MONO_HLSB)
    '''
    fbuf = FrameBuffer(icons.menu_icons[options[opt]], 32, 32, MONO_HLSB)
    p.oled.blit(fbuf, 48, 16)

    # Draw option label centered at bottom
    if len(options) > opt:
        label = options[opt]
    else:
        label = "Unknown App"
    x = (128 - len(label) * 8) // 2
    p.oled.text(label, x, 56)

    # Left arrow
    p.oled.line(4, 32, 12, 24, 1)
    p.oled.line(4, 32, 12, 40, 1)
    p.oled.line(12, 24, 12, 40, 1)

    # Right arrow
    p.oled.line(124, 32, 116, 24, 1)
    p.oled.line(124, 32, 116, 40, 1)
    p.oled.line(116, 24, 116, 40, 1)

    p.oled.show()

    
# Show menu initially

draw_menu(option)
# Main loop
while True:
    if p.pins[1].value() == 0:  # GP3 = Next
        option = (option + 1) % len(options)
        draw_menu(option)
        p.play_tone(1000, 0.05)
        p.wait_for_release(p.pins[1])

    if p.pins[2].value() == 0:  # GP4 = Previous
        option = (option - 1) % len(options)
        draw_menu(option)
        p.play_tone(800, 0.05)
        p.wait_for_release(p.pins[2])

    if p.pins[0].value() == 0:  # GP2 = Select
        p.play_tone(1200, 0.05)
        p.wait_for_release(p.pins[0])
        apps[options[option]]()
        draw_menu(option)
        
    if p.pins[4].value() == 0:  # SOS
        if sos_hold >= 5:
            def dot():
                p.play_tone(1650, 0.05)
                utime.sleep(0.05)
            def dash():
                p.play_tone(1650, 0.15)
                utime.sleep(0.05)
            p.oled.fill(0)
            p.oled.text("SOS triggered", 0, 0)
            p.oled.text("Release to", 0, 10)
            p.oled.text("activate,", 0, 20)
            p.oled.text("Then hold", 0, 30)
            p.oled.text("to deactivate", 0, 40)
            p.oled.show()
            p.wait_for_release(p.pins[4])
            while not p.pins[4].value() == 0:
                dot()
                dot()
                dot()
                utime.sleep(0.1)
                dash()
                dash()
                dash()
                utime.sleep(0.1)
                dot()
                dot()
                dot()
                utime.sleep(0.3)
            p.oled.fill(0)
            p.oled.text("SOS DEACTIVATED", 0, 0)
            p.oled.text("Release to exit", 0, 10)
            p.oled.show()
            p.wait_for_release(p.pins[4])
            draw_menu(option)
        else:
            sos_hold +=1
            p.play_tone(1650, 0.05)
            utime.sleep(0.95)
    elif sos_hold != 0:
        sos_hold = 0;