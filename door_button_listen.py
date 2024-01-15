import RPi.GPIO as GPIO
import time
# Use GPIO numbers not pin numbers
try:
    GPIO.setmode(GPIO.BCM)
    # ----- Pins
    DOOR_BUTTON_PIN = 15 # Has a 1K resistor and uses this 3.3V pin, the other pin is set to ground  (physical pin 10)

    def button_callback(channel):
        print("Button was pressed")

    print("Test")

    GPIO.setup(DOOR_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.remove_event_detect(DOOR_BUTTON_PIN)
    GPIO.add_event_detect(DOOR_BUTTON_PIN,GPIO.RISING,callback=button_callback)
    while True:
        time.sleep(1)
finally:
    GPIO.cleanup() # Clean up

