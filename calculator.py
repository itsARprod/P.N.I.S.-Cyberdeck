from machine import Pin, I2C, PWM
import ssd1306
import utime
import p

def run_calculator():
    number1 = 0
    number2 = 0
    operators = ["+", "-", "*", "/"]
    operator_index = 0
    selected = 0  # 0=num1, 1=op, 2=num2, 3=equals

    def draw():
        p.oled.fill(0)

        x_num1 = 0
        x_op = 38
        x_num2 = 66
        x_eq = 100
        p.oled.text("B/Y - Change", 0, 0)
        p.oled.text(str(number1), x_num1, 32)
        p.oled.text(operators[operator_index], x_op, 32)
        p.oled.text(str(number2), x_num2, 32)
        p.oled.text("=", x_eq, 32)

        def draw_triangle(x0, y0, x1, y1, x2, y2):
            p.oled.line(x0, y0, x1, y1, 1)
            p.oled.line(x1, y1, x2, y2, 1)
            p.oled.line(x2, y2, x0, y0, 1)

        def draw_selector(x):
            draw_triangle(x + 4, 18, x + 8, 14, x + 12, 18)
            draw_triangle(x + 4, 46, x + 8, 50, x + 12, 46)

        if selected == 0:
            draw_selector(x_num1)
        elif selected == 1:
            draw_selector(x_op)
        elif selected == 2:
            draw_selector(x_num2)
        elif selected == 3:
            draw_selector(x_eq)

        p.oled.show()

    def calculate():
        nonlocal number1
        op = operators[operator_index]
        try:
            if op == "+":
                number1 = number1 + number2
            elif op == "-":
                number1 = number1 - number2
            elif op == "*":
                number1 = number1 * number2
            elif op == "/":
                number1 = number1 // number2 if number2 != 0 else 0
        except:
            number1 = 0
        p.play_tone(800, 0.05)
        p.play_tone(1200, 0.05)
    draw()

    while True:
        if p.pins[0].value() == 0:  # UP
            if selected == 0:
                i = 0
                while p.pins[0].value() == 0:
                    i += 1
                    number1 += 1
                    p.play_tone(abs(number1) * 10 + 200, 0.05)
                    utime.sleep((0.05 / i) * 2)
                    draw()
            elif selected == 1:
                operator_index = (operator_index + 1) % len(operators)
                p.play_tone(operator_index * 50 + 200, 0.05)
                p.wait_for_release(p.pins[0])
            elif selected == 2:
                i = 0
                while p.pins[0].value() == 0:
                    i += 1
                    number2 += 1
                    p.play_tone(abs(number2) * 10 + 200, 0.05)
                    utime.sleep((0.05 / i) * 2)
                    draw()
            elif selected == 3:
                calculate()
                p.wait_for_release(p.pins[0])
            draw()
            

        if p.pins[3].value() == 0:  # DOWN
            if selected == 0:
                i = 0
                while p.pins[3].value() == 0:
                    i += 1
                    number1 -= 1
                    p.play_tone(abs(number1) * 10 + 200, 0.05)
                    utime.sleep((0.05 / i) * 2)
                    draw()
            elif selected == 1:
                operator_index = (operator_index - 1) % len(operators)
                p.play_tone(operator_index * 50 + 200, 0.05)
                p.wait_for_release(p.pins[3])
            elif selected == 2:
                i = 0
                while p.pins[3].value() == 0:
                    i += 1
                    number2 -= 1
                    p.play_tone(abs(number2) * 10 + 200, 0.05)
                    utime.sleep((0.05 / i) * 2)
                    draw()
            elif selected == 3:
                calculate()
                p.wait_for_release(p.pins[3])
            draw()
            

        if p.pins[1].value() == 0:  # RIGHT
            selected = (selected + 1) % 4
            p.play_tone(1000, 0.05)
            draw()
            p.wait_for_release(p.pins[1])

        if p.pins[2].value() == 0:  # LEFT
            selected = (selected - 1) % 4
            p.play_tone(800, 0.05)
            draw()
            p.wait_for_release(p.pins[2])

        if p.pins[4].value() == 0:  # GP6 to exit
            p.play_tone(400, 0.1)
            break

