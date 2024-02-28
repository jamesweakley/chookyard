import rpyc
hardware_service = rpyc.connect("localhost", 18861).root
print(hardware_service.get_door_status())