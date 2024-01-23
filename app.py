from picamera2 import Picamera2, Preview
import time
import os
import datetime
import streamlit as st
import RPi.GPIO as GPIO
import libcamera
from gpiozero import MotionSensor


# ----- Pins
DOOR_SENSOR_PIN = 7 # this is a reed switch, the other pin is ground
# Linear actuator is driven by this H-Bridge:
# https://core-electronics.com.au/attachments/localcontent/4489_datasheet-l9110_20452935fd7.pdf
LINEAR_ACTUATOR_A = 5
LINEAR_ACTUATOR_B = 6
DOOR_BUTTON_PIN = 15 # Has a 1K resistor and uses this 3.3V pin, the other pin is set to ground  (physical pin 10)
LED_EYES_PIN = 18 # Anode side of LED, the other pin is set to ground with a 300 Ohm resistor
WHITE_LED_PIN = 4 # Anode side of LED, the other pin is set to ground with a 300 Ohm resistor

CAMERA_IMAGE_PATH = "/tmp/camera.jpg"

st.set_page_config(page_title="Chooks", page_icon="🐔", layout="centered")

def get_door_status():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    door_status = "Open" if GPIO.input(DOOR_SENSOR_PIN)==1 else "Closed"
    return door_status

def open_door():
    with st.status("Opening door...") as status:
        st.write("Setting output pins")
        # Set the signal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LINEAR_ACTUATOR_A, GPIO.OUT)
        GPIO.setup(LINEAR_ACTUATOR_B, GPIO.OUT)
        GPIO.output(LINEAR_ACTUATOR_B, GPIO.LOW)
        GPIO.output(LINEAR_ACTUATOR_A, GPIO.HIGH)
        # wait until the door opens
        # we want to deliberately wait about 6 seconds so that the next
        # camera shot is of the fully open door
        for i in range(6):
            st.write(f"Waited {i} seconds, door is {get_door_status()}")
            time.sleep(1)
        if get_door_status()=="Closed":
            status.update(label="Door did not open",state="error")
        else:
            status.update(label="Door opened",state="complete")

def close_door():
    with st.status("Closing door...") as status:
        st.write("Setting output pins")
        # Set the signal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LINEAR_ACTUATOR_A, GPIO.OUT)
        GPIO.setup(LINEAR_ACTUATOR_B, GPIO.OUT)
        GPIO.output(LINEAR_ACTUATOR_B, GPIO.HIGH)
        GPIO.output(LINEAR_ACTUATOR_A, GPIO.LOW)
        seconds_remaining = 10 # if it takes longer than this, something is wrong
        while get_door_status()=="Open" and seconds_remaining > 0:
            st.write(f"Waiting {seconds_remaining} more seconds, door is {get_door_status()}")
            time.sleep(1)
            seconds_remaining = seconds_remaining - 1
        if get_door_status()=="Open":
            status.update(label="Door did not close",state="error")
        else:
            status.update(label="Door closed",state="complete")


def door_button_callback(channel):
    # append to ./logs/door_button.log
    with open(os.path.join('logs','door_button.log'), 'a') as f:
        f.write(f"{datetime.datetime.now().isoformat()}: Door button pressed, channel: {channel}")
    if get_door_status()=='Open':
        close_door()
    else:
        open_door()

# do this once only
@st.cache_resource
def init_pins():
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(WHITE_LED_PIN, GPIO.OUT)
    GPIO.setup(DOOR_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.remove_event_detect(DOOR_BUTTON_PIN)
    GPIO.add_event_detect(DOOR_BUTTON_PIN,GPIO.FALLING,callback=door_button_callback)
    return True
init_pins()


# Cache the camera, it needs to be a singleton
@st.cache_resource
def get_camera():
    picam2 = Picamera2()
    config = picam2.create_still_configuration(transform=libcamera.Transform(hflip=1, vflip=1))
    picam2.configure(config)
    picam2.start()
    return picam2


def get_red_eyes_status():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_EYES_PIN, GPIO.OUT)
    led_status = "On" if GPIO.input(LED_EYES_PIN)==1 else "Off"
    return led_status

def red_eyes_on():
    # Set the signal
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_EYES_PIN, GPIO.OUT)
    GPIO.output(LED_EYES_PIN, GPIO.HIGH)

def update_camera_image():
    picam2 = get_camera()
    picam2.capture_file(CAMERA_IMAGE_PATH)

current_door_status = get_door_status()
st.markdown(f"Door status: `{current_door_status}`")
col1,col2,col3 = st.columns(3)
with col1:
    if st.button(label="Refresh",key="refresh"):
        update_camera_image()
        st.rerun()

with col2:
    st.button(label="Open Door",
            key="open_door",
            #disabled=current_door_status=="Open",
            on_click=open_door)
with col3:
    st.button(label="Close Door",
            key="close_door",
            #disabled=current_door_status=="Closed",
            on_click=close_door)

if not os.path.exists(CAMERA_IMAGE_PATH):
    update_camera_image()

st.image(CAMERA_IMAGE_PATH)

st.markdown(f"Red eyes: `{get_red_eyes_status()}`")

GPIO.cleanup()

