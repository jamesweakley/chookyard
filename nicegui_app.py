from nicegui import ui
import os
import RPi.GPIO as GPIO
import rpyc
import arrow
from hardware_service import HardwareService

CAMERA_IMAGE_PATH = "/tmp/camera.jpg"

#st.set_page_config(page_title="Chooks", page_icon="🐔", layout="centered")
hardware_service:HardwareService = rpyc.connect("localhost", 18861).root

async def open_door():
    hardware_service.open_door()
    hardware_service.capture_camera_image()

async def close_door():
    hardware_service.close_door()
    hardware_service.capture_camera_image()

current_door_status = hardware_service.get_door_status()

if not os.path.exists(CAMERA_IMAGE_PATH):
    hardware_service.capture_camera_image()

# get the file modified time of the image, calculate how long ago it was taken
mod_time = os.path.getmtime(CAMERA_IMAGE_PATH)
    
# Use arrow to get a human-readable string
mod_time_readable = arrow.get(mod_time).humanize()

async def refresh():
    hardware_service.capture_camera_image()
    image.force_reload()
    mod_time = os.path.getmtime(CAMERA_IMAGE_PATH)
    mod_time_readable = arrow.get(mod_time).humanize()
    photo_taken_label.set_text(f'Photo taken: {mod_time_readable}')

# UI Elements
ui.label(f'Door status: {hardware_service.get_door_status()}')
with ui.row():
    ui.button('Refresh', on_click=refresh)

    ui.button('Open Door', on_click=open_door)
    ui.button('Close Door', on_click=close_door)

image = ui.image(CAMERA_IMAGE_PATH)
photo_taken_label = ui.label(f'Photo taken: {mod_time_readable}')
ui.label(f'Red eyes: {hardware_service.get_red_eyes_status()}')

ui.run()

GPIO.cleanup()

