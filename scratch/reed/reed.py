import time
import RPi.GPIO as GPIO


REED_SWITCH = 21


def main():
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    GPIO.setwarnings(True)
    GPIO.setup(REED_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    val = None
    while True:
        new_val = GPIO.input(REED_SWITCH)
        if new_val is not val:
            val = new_val
            print(val)
        time.sleep(0.1)

    GPIO.cleanup()

if __name__ == '__main__':
    main()
