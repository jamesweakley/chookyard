import RPi.GPIO as GPIO
# Use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)
# ----- Pins
DOOR_SENSOR_PIN = 7 # this is a reed switch, the other pin is ground
# Linear actuator is driven by this H-Bridge:
# https://core-electronics.com.au/attachments/localcontent/4489_datasheet-l9110_20452935fd7.pdf
LINEAR_ACTUATOR_A = 5
LINEAR_ACTUATOR_B = 6
DOOR_BUTTON_PIN = 10 # Has a 1K resistor and uses this 3.3V pin, the other pin is set to ground  (physical pin 10)

def get_door_status():
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    door_status = "Open" if GPIO.input(DOOR_SENSOR_PIN)==1 else "Closed"
    return door_status

def open_door():
    # Set pins as output pins
    GPIO.setup(LINEAR_ACTUATOR_A, GPIO.OUT)
    GPIO.setup(LINEAR_ACTUATOR_B, GPIO.OUT)
    # Set the signal
    GPIO.output(LINEAR_ACTUATOR_A, GPIO.LOW)
    GPIO.output(LINEAR_ACTUATOR_B, GPIO.HIGH)

def close_door():
    # Set pins as output pins
    GPIO.setup(LINEAR_ACTUATOR_A, GPIO.OUT)
    GPIO.setup(LINEAR_ACTUATOR_B, GPIO.OUT)
    # Set the signal
    GPIO.output(LINEAR_ACTUATOR_A, GPIO.HIGH)
    GPIO.output(LINEAR_ACTUATOR_B, GPIO.LOW)
