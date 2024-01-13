import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
DOOR_SENSOR_PIN = 7 
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
print("Open" if GPIO.input(DOOR_SENSOR_PIN)==1 else "Closed")
