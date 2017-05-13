#!/usr/bin/python
#
# HD44780 LCD Test Script for
# Raspberry Pi
#
# Author : Matt Hawkins + Texy
# Site   : http://www.raspberrypi-spy.co.uk
#
# Date   : 2/12/2012
#
# uses RPi.GPIO to drive the LCD and
# wiringpi to drive the backlight LED via hardware PWM
# this version to be used with TKinter
# this version for v2 rpi only

# import
import RPi.GPIO as GPIO
import time
import wiringpi

# Define GPIO to LCD mapping
LCD_RS = 17
LCD_E = 4
LCD_D4 = 24
LCD_D5 = 22
LCD_D6 = 23
LCD_D7 = 27  # use 27 for v2 rpi, or 21 for v1 rpi
LCD_LED = 18

# Define some device constants
LCD_WIDTH = 20  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005


def main():
    # Main program block
    # Initialise display
    lcd_init()

    # Send some test
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("wiringpi and")
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("RPi.GPIO 2gether")


def line1txt(message1):
    message1 = message1[:-1]  # remove last char (whitespace)
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(message1)


def line2txt(message2):
    message2 = message2[:-1]
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(message2)


def line3txt(message3):
    message3 = message3[:-1]
    lcd_byte(LCD_LINE_3, LCD_CMD)
    lcd_string(message3)


def line4txt(message4):
    message4 = message4[:-1]
    lcd_byte(LCD_LINE_4, LCD_CMD)
    lcd_string(message4)


def cls():
    lcd_byte(0x01, LCD_CMD)


def led(led_value):
    wiringpi.pwmWrite(LCD_LED, led_value)


# print led_value


def switch_led(led_value):
    if led_value == 0:
        wiringpi.pinMode(LCD_LED, 1)
        wiringpi.digitalWrite(LCD_LED, 0)
    else:
        wiringpi.pinMode(LCD_LED, 2)
        wiringpi.pwmWrite(LCD_LED, 128);


def lcd_init():
    # Initialise display
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(LCD_LED, 2)  # LED set up as PWM
    wiringpi.pwmWrite(LCD_LED, 128)
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    cls()


def lcd_string(message):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


if __name__ == '__main__':
    main()
