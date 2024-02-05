import time
import os
import datetime
import RPi.GPIO as GPIO
import libcamera
from gpiozero import MotionSensor

GPIO.setmode(GPIO.BCM)
LED_EYES_PIN = 24 # Anode side of LED, the other pin is set to ground with a 300 Ohm resistor
MOTION_SENSOR_PIN = 17
GPIO.setup(LED_EYES_PIN, GPIO.OUT)


def get_red_eyes_status():
    led_status = "On" if GPIO.input(LED_EYES_PIN)==1 else "Off"
    return led_status

from gpiozero import MotionSensor

def motion_action():
	current_hour = datetime.datetime.now().hour
	if current_hour > 7 and current_hour < 19:
		print("skipping due to daytime")
		return
	print("motion detected, turning on eyes")
	GPIO.output(LED_EYES_PIN, GPIO.HIGH)
	for i in range(5):
		# do five sets of eye blinks, 3 seconds apart
		time.sleep(3)
		GPIO.output(LED_EYES_PIN, GPIO.LOW)
		time.sleep(0.1)
		GPIO.output(LED_EYES_PIN, GPIO.HIGH)
	time.sleep(5)
	print("turning off eyes")
	GPIO.output(LED_EYES_PIN, GPIO.LOW)

pir = MotionSensor(pin=MOTION_SENSOR_PIN)
pir.when_motion=motion_action

while True:
	time.sleep(1)

GPIO.output(LED_EYES_PIN, GPIO.LOW)
