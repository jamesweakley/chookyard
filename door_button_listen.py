from picamera2 import Picamera2, Preview
import time
import os
import datetime
import RPi.GPIO as GPIO
import libcamera
from gpiozero import MotionSensor

# Use GPIO numbers not pin numbers
# ----- Pins
DOOR_SENSOR_PIN = 7 # this is a reed switch, the other pin is ground
# Linear actuator is driven by this H-Bridge:
# https://core-electronics.com.au/attachments/localcontent/4489_datasheet-l9110_20452935fd7.pdf
LINEAR_ACTUATOR_A = 5
LINEAR_ACTUATOR_B = 6
DOOR_BUTTON_PIN = 15 # Has a 1K resistor and uses this 3.3V pin, the other pin is set to ground  (physical pin 10)
LED_EYES_PIN = 24 # Anode side of LED, the other pin is set to ground with a 300 Ohm resistor
DOOR_LATCH_PIN = 18 # 5V relay opening 24V latch

last_button_press = datetime.datetime.now() - datetime.timedelta(seconds=5)

def get_door_status():
    door_status = "Open" if GPIO.input(DOOR_SENSOR_PIN)==1 else "Closed"
    return door_status

def get_red_eyes_status():
    led_status = "On" if GPIO.input(LED_EYES_PIN)==1 else "Off"
    return led_status

def close_door():
    #Set the signal
    print("closing door")
    GPIO.output(LINEAR_ACTUATOR_A, GPIO.LOW)
    GPIO.output(LINEAR_ACTUATOR_B, GPIO.HIGH)

def open_door():
    print("opening door")
    hold_latch()
    #Set the signal
    GPIO.output(LINEAR_ACTUATOR_A, GPIO.HIGH)
    GPIO.output(LINEAR_ACTUATOR_B, GPIO.LOW)
    time.sleep(3)
    release_latch()

def hold_latch():
    GPIO.output(DOOR_LATCH_PIN, GPIO.HIGH)

def release_latch():
    GPIO.output(DOOR_LATCH_PIN, GPIO.LOW)

def door_button_callback(channel):
    global last_button_press
    time_since_last_press = datetime.datetime.now() - last_button_press
    if time_since_last_press.seconds < 5:
        print(f"too soon since last button press: {time_since_last_press.seconds} seconds")
        return
    last_button_press = datetime.datetime.now()
    # append to ./logs/door_button.log
    with open(os.path.join('logs','door_button.log'), 'a') as f:
        f.write(f"{datetime.datetime.now().isoformat()}: Door button pressed, channel: {channel}\r\n")
    if get_door_status()=='Open':
        #open_door()
        close_door()
    else:
        open_door()

GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LINEAR_ACTUATOR_A, GPIO.OUT)
GPIO.setup(LINEAR_ACTUATOR_B, GPIO.OUT)

GPIO.setup(DOOR_LATCH_PIN,GPIO.OUT)

GPIO.setup(DOOR_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.remove_event_detect(DOOR_BUTTON_PIN)
GPIO.add_event_detect(DOOR_BUTTON_PIN,GPIO.FALLING,callback=door_button_callback)

#GPIO.wait_for_edge(DOOR_BUTTON_PIN,GPIO.RISING,bouncetime=300)
#print(GPIO.input(DOOR_BUTTON_PIN))
while True:
    time.sleep(1)

GPIO.cleanup()

