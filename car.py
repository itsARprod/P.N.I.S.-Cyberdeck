from machine import Pin
import utime
import os
import p
import icons
import random
from framebuf import FrameBuffer, MONO_HLSB
import math

SAVE_FILE = "saves.txt"

def run_car():
    from random import randint

    # Load save data into a dictionary
    def load_saves():
        saves = {}
        try:
            with open(SAVE_FILE, "r") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        saves[k] = int(v)
        except:
            saves["chigh_score"] = 0
        return saves

    # Save the updated dictionary back to file
    def save_saves(saves):
        with open(SAVE_FILE, "w") as f:
            for k, v in saves.items():
                f.write(f"{k}={v}\n")

    saves = load_saves()
    chigh_score = saves.get("chigh_score", 0)

    def draw(xpos, ypos, speed, spikex, spikey):
        p.oled.fill(0)
        y = (ypos) % 64
        p.oled.line(64, y, 64, y + 8, 1)
        y = (ypos - 16) % 64
        p.oled.line(64, y, 64, y + 8, 1)
        y = (ypos - 32) % 64
        p.oled.line(64, y, 64, y + 8, 1)
        y = (ypos - 48) % 64
        p.oled.line(64, y, 64, y + 8, 1)
        y = (ypos - 64) % 64
        p.oled.line(64, y, 64, y + 8, 1)
        fbuf = FrameBuffer(icons.car_player, 16, 16, MONO_HLSB)
        p.oled.blit(fbuf, xpos - 8, 48)
        fbuf = FrameBuffer(icons.car_spike, 32, 16, MONO_HLSB)
        p.oled.blit(fbuf, spikex - 16, spikey - 8)
        p.oled.text(str(score), 0, 0)
        p.oled.show()
        
    def game_over_screen(score):
        p.oled.fill(0)
        p.oled.text("GAME OVER", 20, 16)
        p.oled.text(f"Score: {score}", 10, 32)
        p.oled.text(f"High: {chigh_score}", 10, 42)
        p.oled.text("UP = Restart", 10, 54)
        p.oled.show()

    while True:
        score = 0
        dead = False
        xpos = 64
        ypos = 48
        speed = 0
        spikey = 72
        spikex = 0
        while not dead:
            if p.pins[3].value() == 0:  # DOWN
                if speed > 0.2:
                    speed -= 0.2
            else:
                if speed < 3:
                    speed += 0.2
            if p.pins[1].value() == 0:  # RIGHT
                xpos += 2
            elif p.pins[2].value() == 0:  # LEFT
                xpos -= 2
            elif p.pins[4].value() == 0:  # EXIT
                return
            ypos = math.floor(ypos + speed)
            if spikey >= 200:
                spikex = random.randint(16, 112)
                spikey = -8
                score += 1
                p.play_tone(1200, 0.05)
            else:
                spikey += math.floor(speed)
            if (xpos < (spikex + 16) and xpos > (spikex - 16)
            and 48 < (spikey + 8) and 48 > (spikey - 8)):
                dead = True
                p.play_tone(400, 0.1)
            draw(xpos, ypos, speed, spikex, spikey)
            
            
        if score > chigh_score:
            chigh_score = score
            saves["chigh_score"] = chigh_score
            save_saves(saves)

        game_over_screen(score)

        while True:
            if p.pins[0].value() == 0:  # UP = restart
                p.play_tone(1000, 0.1)
                while p.pins[0].value() == 0:
                    utime.sleep(0.01)
                break
            elif p.pins[4].value() == 0:  # GP6 = Exit
                p.play_tone(400, 0.1)
                return


