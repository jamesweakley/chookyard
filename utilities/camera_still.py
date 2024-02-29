import rpyc
from hardware_service import HardwareService

hardware_service:HardwareService = rpyc.connect("localhost", 18861).root
hardware_service.capture_camera_image()