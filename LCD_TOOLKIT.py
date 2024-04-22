from machine import Pin, SoftI2C
import machine
from time import sleep
import time
from math import floor
#LCD Class created by liyuanhe221
#https://github.com/liyuanhe211/Micropython_LCD1602_LCD2004_I2C_Lib
#LCD_TOOLS class created by Loganius_II
#https://github.com/loganius-ii

#MUST run I2C_SCAN in order for other functions to work
def I2C_SCAN(lcd_data: tuple[int,int,int]) -> str:
    scl, sda, freq = lcd_data
    device_list = []
    sdaPIN=machine.Pin(sda)
    sclPIN=machine.Pin(scl)
    i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=freq)
    devices = i2c.scan()
    if len(devices) != 0:
        for device in devices:
            device_list.append(hex(device))
        return device_list
    else:
        return 'No I2C device found'
    

class LCD():
    def __init__(self, i2c):

        # board definition
        # P0: RS
        # P1: R/W
        # P2: E
        # P3: --
        # P4-P7: DB4-DB7

        self.i2c = i2c
        print('(Re)Initializing...')
        scan_result = i2c.scan()
        while not scan_result:
            print("Cannot Locate I2C Device")
            time.sleep_ms(10)
            scan_result = i2c.scan()
        self.LCD_I2C_ADDR = i2c.scan()[0]
        self.bufs = []  # a list of bytes, created as writing things all in one go with i2c.writeto is more efficient than writing each byte
        self.BK = 0x08
        self.RS = 0x00
        self.E = 0x04

        self.queue(0x30)  # 0011
        self.execute()
        time.sleep_ms(5)
        self.queue(0x30)  # 0011
        self.execute()
        time.sleep_ms(5)
        self.queue(0x20)  # 0010
        self.execute()
        time.sleep_ms(5)
        self.add_command(0x28,run=True)  # 0010   1000
        self.on()
        self.add_command(0x06)  # 0000   0110
        self.add_command(0x01)  # 0000   0001
        self.execute()

    def queue(self, dat):
        '''
        Add data to queue, wait execution
        :param dat: 8-bit data, first 4 bit is D7-D4, Last 4 bit is NC, E, RW, RS
        :return:
        '''
        
        dat = dat & 0xF0
        dat |= self.BK
        dat |= self.RS
        
        self.bufs.append(dat | 0x04) # enable high
        self.bufs.append(dat) # enable low
            
    def execute(self):
        try:
            bytearray_to_write = bytearray(len(self.bufs))
            for i in range(len(self.bufs)):
                bytearray_to_write[i] = self.bufs[i]
            self.i2c.writeto(self.LCD_I2C_ADDR, bytearray_to_write)
            self.bufs=[]
            time.sleep_us(50)
        except Exception as e:
            print(e)

    def add_command(self, cmd, run=False):
        self.RS = 0
        # I2C chip only has 8 bit, so only 4 bit can be used for data, thus the data needs to be send in two parts
        self.queue(cmd)
        self.queue(cmd << 4)
        if run:
            self.execute()

    def add_data(self, dat):
        self.RS = 1
        # I2C chip only has 8 bit, so only 4 bit can be used for data, thus the data needs to be send in two parts
        self.queue(dat)
        self.queue(dat << 4)

    def clear(self):
        self.add_command(1,run=True)

    def backlight(self, on):
        if on:
            self.BK = 0x08
        else:
            self.BK = 0
        self.add_command(0,run=True)

    def on(self):
        self.add_command(0x0C,run=True)  # 0000 1100 Turn on screen,  turn cursor off, turn blink off

    def off(self):
        self.add_command(0x08,run=True)  # 0000 1000 Turn off screen, turn cursor off, turn blink off

    def shl(self):
        self.add_command(0x18,run=True)

    def shr(self):
        self.add_command(0x1C,run=True)

    def char(self, ch, x=-1, y=0):
        if x >= 0:
            if y == 0:
                a = 0x80
            if y == 1:
                a = 0xC0
            if y == 2:
                a = 0x80 + 20
            if y == 3:
                a = 0xC0 + 20
            a += x
            self.add_command(a)
        self.add_data(ch)

    def puts(self, s, y=0, x=0):
        '''

        :param s: string, ascii only
        :param y: row (you need to write reasonable number to this parameter yourself)
        :param x: column (you need to write reasonable number to this parameter yourself)
        :return:
        '''
        try:
            if len(s) > 0:
                self.char(ord(s[0]), x, y)
                for i in range(1, len(s)):
                    self.char(ord(s[i]))
        except Exception as e:
            print(e)
        self.execute()

    def create_charactor(self, ram_position, char):
        '''

        :param position: int, 0-7
        :param char: 8 bytes
        :return:
        '''

        assert len(char)==8
        ram_position &= 0x7;
        set_CGRAM_address = 0x40
        self.add_command(set_CGRAM_address | (ram_position << 3))
        for i in range(8):
            self.add_data(char[i])
        self.execute()





class LCD_TOOLS:
    def __init__(self, rows, columns, LCD_tuple):
        self.rows = rows
        self.columns = columns
        self.LCD_tuple = LCD_tuple
        if not isinstance(self.LCD_tuple, tuple):
            raise('lcd parameter must be type tuple')
        self.scl, self.sda, self.freq = LCD_tuple
        self.LCD_screen = LCD(SoftI2C(scl=Pin(self.scl), sda=Pin(self.sda), freq = self.freq))
        
    def clearLCD(self) -> None:
        for row in range(self.rows):
            self.LCD_screen.puts(' '*self.columns, row)
    def dump_text(self, text: str,row=0,column=0) -> None:
        characters_used = len(text) + column
        if characters_used  > self.columns:
            extra_letters = characters_used - self.columns
            index_of_split = len(text) - extra_letters
            self.LCD_screen.puts(text[:index_of_split], row, column)
            self.LCD_screen.puts(text[index_of_split:], row+1, 0)
        else:
            self.LCD_screen.puts(text, row, column)
    def middle(self,text) -> int:
        return floor(abs(self.columns/2 - len(text)))
# LCD_TOOLS Usage
#===============================================
def main() -> None:
    #long way to initialize lcd screen
    lcd_screen = LCD(SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000))
    btn = Pin(13, Pin.IN, Pin.PULL_DOWN)
    lcd_screen.puts("hello")
    sleep(1)
    #short way to initialize lcd screen
    #LCD_TOOLS(rows,columns, tuple[scl pin, sda pin, freq]
    lcd_screen_tool = LCD_TOOLS(2,16, (5,4,100000))
    lcd_screen_tool.clearLCD()
    sleep(1)
    lcd_screen_tool.dump_text('hello guys', 0, 14)
    sleep(2)
#===============================================
#LCD Usage (using button)
#===============================================
'''
for i in range(10):
    if btn.value() == 1:
        button_state = 'Button is pressed'
    else:
        button_state = 'Button not pressed'
        
    lcd_screen.puts(button_state)
    sleep(0.5)
    
clearLCD(2, 16)
'''
#===============================================
if __name__ == '__main__':
    main()