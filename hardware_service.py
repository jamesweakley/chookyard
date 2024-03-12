import rpyc
from rpyc.utils.server import ThreadedServer
from picamera2 import Picamera2, Preview
import time
import logging
import datetime
import RPi.GPIO as GPIO
import libcamera
from gpiozero import MotionSensor
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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
CAMERA_IMAGE_PATH = "/tmp/camera.jpg"

#last_button_press = datetime.datetime.now() - datetime.timedelta(seconds=5)

class HardwareService(rpyc.Service):
    def __init__(self) -> None:
        super().__init__()
        logging.info("Starting hardware service")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(LINEAR_ACTUATOR_A, GPIO.OUT)
        GPIO.setup(LINEAR_ACTUATOR_B, GPIO.OUT)
        GPIO.setup(DOOR_LATCH_PIN,GPIO.OUT)
        GPIO.setup(LED_EYES_PIN, GPIO.OUT)
        logging.info("Initializing camera...")
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration(transform=libcamera.Transform(hflip=1, vflip=1))
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(1)
    
    def test(self) -> bool:
        return True

    def get_door_status(self) -> str:
        door_status = "Open" if GPIO.input(DOOR_SENSOR_PIN)==1 else "Closed"
        return door_status

    def capture_camera_image(self):
        self.picam2.capture_file(CAMERA_IMAGE_PATH)

    def get_red_eyes_status(self) -> str:
        led_status = "On" if GPIO.input(LED_EYES_PIN)==1 else "Off"
        return led_status

    def close_door(self):
        #Set the signal
        print("closing door")
        try:
            GPIO.output(LINEAR_ACTUATOR_B, GPIO.HIGH)
            GPIO.output(LINEAR_ACTUATOR_A, GPIO.LOW)
            seconds_remaining = 10 # if it takes longer than this, something is wrong
            while self.get_door_status()=="Open" and seconds_remaining > 0:
                seconds_remaining = seconds_remaining - 1
                print(f"Waiting {seconds_remaining} more seconds, door is {self.get_door_status()}")
                if seconds_remaining == 8:
                    self.hold_latch()
                time.sleep(1)
            if self.get_door_status()=="Open":
                return "Door did not close"
            else:
                return "Door closed"
        finally:
            self.release_latch()



    def open_door(self):
        print("opening door")
        self.hold_latch()
        #Set the signal
        GPIO.output(LINEAR_ACTUATOR_A, GPIO.HIGH)
        GPIO.output(LINEAR_ACTUATOR_B, GPIO.LOW)
        time.sleep(10)
        self.release_latch()

    def hold_latch(self):
        GPIO.output(DOOR_LATCH_PIN, GPIO.HIGH)

    def release_latch(self):
        GPIO.output(DOOR_LATCH_PIN, GPIO.LOW)

    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

if __name__ == "__main__":
    service = HardwareService()
    try:
        server = ThreadedServer(service, port=18861, protocol_config={
            'allow_public_attrs': True,
        })
        server.start()
    finally:
        GPIO.cleanup()
        service.picam2.stop()
