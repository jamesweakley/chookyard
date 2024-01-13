from picamera2 import Picamera2, Preview
import time
import streamlit as st
import RPi.GPIO as GPIO
# Use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)
# ----- Pins
DOOR_SENSOR_PIN = 7 # this is a reed switch, the other pin is ground
# Linear actuator is driven by this H-Bridge:
# https://core-electronics.com.au/attachments/localcontent/4489_datasheet-l9110_20452935fd7.pdf
LINEAR_ACTUATOR_A = 5
LINEAR_ACTUATOR_B = 6

# Cache the camera, it needs to be a singleton
@st.cache_resource
def get_camera():
    picam2 = Picamera2()
    picam2.start()
    return picam2

def get_door_status():
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    door_status = "Open" if GPIO.input(DOOR_SENSOR_PIN)==1 else "Closed"
    return door_status

def begin_open_door():
    # Set pins as output pins
    GPIO.setup(LINEAR_ACTUATOR_A, GPIO.OUT)
    GPIO.setup(LINEAR_ACTUATOR_B, GPIO.OUT)
    # Set the signal
    GPIO.output(LINEAR_ACTUATOR_A, GPIO.LOW)
    GPIO.output(LINEAR_ACTUATOR_B, GPIO.HIGH)

def begin_close_door():
    # Set pins as output pins
    GPIO.setup(LINEAR_ACTUATOR_A, GPIO.OUT)
    GPIO.setup(LINEAR_ACTUATOR_B, GPIO.OUT)
    # Set the signal
    GPIO.output(LINEAR_ACTUATOR_A, GPIO.HIGH)
    GPIO.output(LINEAR_ACTUATOR_B, GPIO.LOW)

st.markdown(f"Door status: `{get_door_status()}`")
picam2 = get_camera()
picam2.capture_file("camera.jpg")
st.image("camera.jpg")

if st.button(label="Refresh",key="refresh"):
    st.experimental_rerun()

if st.button(label="Open Door",key="open_door"):
    begin_open_door()

if st.button(label="Close Door",key="close_door"):
    begin_close_door()


