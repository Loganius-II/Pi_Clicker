# Pi_Clicker
### Clicking game with Raspberry Pico. I am new to Raspberry Pi's and decided to use some prior knowledge of coding to create a clicker game. I had no internet help and just went off of my own coding experience and had learned how to code onto LCD screens as well.
### I also created my own mini module that I just called LCD_TOOLKIT and added some of my classes and code to another module created by another user (Their credit is in the source code of the module). The module that I created further simplified my process of making Pi Clicker

# Supplies
 - Laptop or computer with Thonny
 - This code is fixed to a 2x16 LCD display
      - I am using a Sainsmart 2004 LCD display (Discontinued :/)
      - This one already has a microcontroller thingy to simplify the output to GND, VCC, SDA, SCL
      - SCL is going to pin 5
      - SDA going to pin 4
 - Some sort of button/switch but a button is prefered
 - Raspberry Pi Pico (I use H)
 - Pins, all of that
 - No resistors

# Features
#### Main features include:
 - Home/main screen
    - There is a SLCTN counter that increments
    - Just hold down the button until the selection gets to the desired menu item
    - 3 Pages/actions
       - RESET, which clears the score
       - PLAY, which is self explainatory
       - HELP, which just displays a tip
          - Hold down button to exit help screen
    - Saving progress; **Hold button down for three seconds to save progress**
    - Thats pretty much it        


