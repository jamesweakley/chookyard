import rpyc
from hardware_service import HardwareService

def get_hardware_service() -> HardwareService:
    hardware_service:HardwareService = rpyc.connect("localhost", 18861).root
    return hardware_service

hs = get_hardware_service()
hs.open_door()
hs.capture_camera_image()

from pushover import Client
client = Client("ueovdt7awncixwx7bgoiz8fp6p9jrr", api_token="am62ab28fb7p389h15v5nnjmcj63oo")
with open('/tmp/camera.jpg', 'rb') as image:
    client.send_message('Door open', attachment=image)
