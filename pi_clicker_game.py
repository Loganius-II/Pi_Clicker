#Button Game
#Objective: get as many clicks as possible
#Hold button for 3 Seconds to save
from machine import Pin
from time import sleep
from LCD_TOOLKIT import LCD, LCD_TOOLS, I2C_SCAN
import asyncio
import utime
LCD_PINS_FREQ = (5,4,100000)



def middle(text: str) -> int:
    return abs(8-len(text))
scan = I2C_SCAN(LCD_PINS_FREQ)
print(scan)
btn = Pin(13, Pin.IN, Pin.PULL_DOWN)
lcd_display = LCD_TOOLS(2,16,LCD_PINS_FREQ)

text = 'Pi Clicker!'
lcd_display.dump_text('Welcome to')
sleep(1)
lcd_display.dump_text(text, 1,lcd_display.middle(text))
sleep(2)
lcd_display.clearLCD()
sleep(0.2)
lcd_display.dump_text('By: Logan')
lcd_display.dump_text('McDermott', 1, lcd_display.middle(text))
sleep(2)

def menu_screen() -> int:
    selection = 1
    while True:
        lcd_display.clearLCD()
        if selection == 1:
            lcd_display.dump_text('1:Play!  3:RESET')
            lcd_display.dump_text('2:Help', 1)
            lcd_display.dump_text('SLCTN:1', 1, 9)
            sleep(2)
            if btn.value() == 1:
                return 1
            else:
                selection = 2
        elif selection == 2:
            lcd_display.dump_text('1:Play!  3:RESET')
            lcd_display.dump_text('2:Help', 1)
            lcd_display.dump_text('SLCTN:2', 1, 9)
            sleep(2)
            if btn.value() == 1:
                return 2
            else:
                selection = 3
        else:
            lcd_display.dump_text('1:Play!  3:RESET')
            lcd_display.dump_text('2:Help', 1)
            lcd_display.dump_text('SLCTN:3', 1, 9)
            sleep(2)
            if btn.value() == 1:
                return 3
            else:
                selection = 1
            
def help_screen() -> None:
    lcd_display.clearLCD()
    sleep(1)
    while btn.value() == 0:
        lcd_display.clearLCD()
        lcd_display.dump_text('HELP: Hold button for 3 seconds')
        sleep(2)
        lcd_display.clearLCD()
        lcd_display.dump_text('to save progress!')
        sleep(2)

def save_game() -> None:
    global pi_clicks
    lcd_display.clearLCD()
    lcd_display.dump_text('Game Saved!', 0, lcd_display.middle('Game Saved!'))
    with open('pi_clicks.txt', 'w') as f:
        f.write(str(pi_clicks))

def three_sec_click(start_time) -> None:
        current_time_ms = utime.ticks_ms()
        elapsed_time = utime.ticks_diff(current_time_ms, start_time)
        return elapsed_time >= 3000

                
        '''
        lcd_display.clear_LCD()
        lcd_display.dump_text('Game Saved!', 0, lcd_display.middle('Game Saved!'))
        with open('pi_clicks.txt', 'w') as f:
            f.write(str(pi_clicks))
        '''
def play_screen() -> None:
    global pi_clicks
    lcd_display.clearLCD()
    sleep(0.6)
    bars = 1
    while bars < 15:     
        lcd_display.clearLCD()
        lcd_display.dump_text(f"[{'\n'*bars}{' '*abs((bars-14))}]",1)
        lcd_display.dump_text('Loading...', 0, lcd_display.middle('Loading...'))  
        bars+=1
        sleep(0.2)
    with open('pi_clicks.txt','r') as f:
        pi_clicks = int(f.readline().strip())
    prev_value = 0
    lcd_display.clearLCD()
    lcd_display.dump_text(f'Pi Clicks: {pi_clicks}')
    while True:
        if btn.value() == 1:
            prev_value = 1
            start_time = utime.ticks_ms()
            held_time = 0
            while btn.value() == 1:
                if held_time >= 3:
                    held_time = 0
                    save_game()
                    utime.sleep(2)
                    break
                utime.sleep(0.01)
                held_time += 0.01
            
        elif btn.value() == 0 and prev_value == 1:
            pi_clicks += 1
            lcd_display.clearLCD()
            lcd_display.dump_text(f'Pi Clicks: {pi_clicks}')
            prev_value = 0
        sleep(0.1)
            
def clear_screen() -> None:
    lcd_display.clearLCD()
    with open('pi_clicks.txt', 'w') as f:
        f.write('0')
    lcd_display.dump_text("SCORE RESET")
    lcd_display.dump_text("SUCCESS!", 1, lcd_display.middle("SUCCESS!"))
    sleep(2)

while True:
    selection = menu_screen()
    lcd_display.clearLCD()
    if selection == 2:
        help_screen()
        continue
    elif selection == 3:
        clear_screen()
        continue
    else:
        play_screen()
        continue