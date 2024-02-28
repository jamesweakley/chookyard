import time
import os
import datetime
import RPi.GPIO as GPIO
import rpyc
from gpiozero import Button

# Use GPIO numbers not pin numbers
DOOR_BUTTON_PIN = 15 # Has a 1K resistor and uses this 3.3V pin, the other pin is set to ground  (physical pin 10)

last_button_press = datetime.datetime.now() - datetime.timedelta(seconds=5)

def door_button_callback():
    global last_button_press
    time_since_last_press = datetime.datetime.now() - last_button_press
    if time_since_last_press.seconds < 5:
        print(f"too soon since last button press: {time_since_last_press.seconds} seconds")
        return
    hardware_service = rpyc.connect("localhost", 18861).root
    last_button_press = datetime.datetime.now()
    # append to ./logs/door_button.log
    with open(os.path.join('logs','door_button.log'), 'a') as f:
        f.write(f"{datetime.datetime.now().isoformat()}: Door button pressed\r\n")
    if hardware_service.get_door_status()=='Open':
        #open_door()
        hardware_service.close_door()
    else:
        hardware_service.open_door()

while True:
    button = Button(DOOR_BUTTON_PIN)
    print("Waiting for button press")
    button.wait_for_press()
    door_button_callback()
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(DOOR_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.remove_event_detect(DOOR_BUTTON_PIN)
#GPIO.add_event_detect(DOOR_BUTTON_PIN,GPIO.FALLING,callback=door_button_callback)

#GPIO.wait_for_edge(DOOR_BUTTON_PIN,GPIO.RISING,bouncetime=300)
#print(GPIO.input(DOOR_BUTTON_PIN))
#while True:
#    time.sleep(1)

#GPIO.cleanup()

