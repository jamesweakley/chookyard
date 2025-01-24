import rpyc
from hardware_service import HardwareService
from dotenv import load_dotenv
import os
load_dotenv()

def get_hardware_service() -> HardwareService:
    hardware_service:HardwareService = rpyc.connect("localhost", 18861).root
    return hardware_service

hs = get_hardware_service()
hs.close_door()
hs.capture_camera_image()

from pushover import Client
client = Client(os.environ['PUSHOVER_USER_KEY'], api_token=os.environ['PUSHOVER_API_KEY'])
#client.send_message("Hello!", title="Hello")
with open('/tmp/camera.jpg', 'rb') as image:
    client.send_message('Door closed', attachment=image)
