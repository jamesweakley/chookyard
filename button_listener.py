import time
import os
import datetime
import RPi.GPIO as GPIO
import rpyc
import sys
import logging
from gpiozero import Button
from hardware_service import HardwareService
# Use GPIO numbers not pin numbers
DOOR_BUTTON_PIN = 15 # Has a 1K resistor and uses this 3.3V pin, the other pin is set to ground  (physical pin 10)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

last_button_press = datetime.datetime.now() - datetime.timedelta(seconds=5)

def door_button_callback():
    #print("pressed")
    #return
    global last_button_press
    time_since_last_press = datetime.datetime.now() - last_button_press
    if time_since_last_press.seconds < 5:
        logging.info(f"too soon since last button press: {time_since_last_press.seconds} seconds")
        return
    hardware_service:HardwareService = rpyc.connect("localhost", 18861).root
    last_button_press = datetime.datetime.now()
    logging.info(f"Door button pressed")
    if hardware_service.get_door_status()=='Open':
        hardware_service.close_door()
    else:
        # don't allow opening the door after hours
        current_hour = datetime.datetime.today().hour
        if current_hour > 22 or current_hour < 6:
            logger.info("Preventing door open at prohibited hours")
        hardware_service.open_door()
#button = Button(DOOR_BUTTON_PIN,hold_time=2)
#while True:
    #button = Button(DOOR_BUTTON_PIN)
#    print("Waiting for button press")
#    print(button.is_pressed)
#    time.sleep(1)
#button.wait_for_press()
    #door_button_callback()
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.remove_event_detect(DOOR_BUTTON_PIN)
#GPIO.add_event_detect(DOOR_BUTTON_PIN,GPIO.FALLING,callback=door_button_callback)

#GPIO.wait_for_edge(DOOR_BUTTON_PIN,GPIO.RISING,bouncetime=300)
#print(GPIO.input(DOOR_BUTTON_PIN))
while True:
    logging.info("waiting for button press edge")
    GPIO.wait_for_edge(DOOR_BUTTON_PIN,GPIO.FALLING)
    time.sleep(1)
    if GPIO.input(DOOR_BUTTON_PIN) == GPIO.LOW:
        print("Button was properly pressed")
    else:
        print("Button was improperly pressed")
    #door_button_callback()
GPIO.cleanup()

