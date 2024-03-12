import os, rpyc
import streamlit as st
from hardware_service import HardwareService

CAMERA_IMAGE_PATH = "/tmp/camera.jpg"
st.set_page_config(page_title="Chooks", page_icon="🐔", layout="centered")

def get_hardware_service() -> HardwareService:
    try:
        hw = get_actual_hardware_service()
        hw.test()
    except:
        get_actual_hardware_service.clear()
        hw = get_actual_hardware_service()
    return hw

@st.cache_resource
def get_actual_hardware_service() -> HardwareService:
    hardware_service:HardwareService = rpyc.connect("localhost", 18861).root
    return hardware_service

def open_door():
    with st.status("Opening door...") as status:
        st.write("Closing door")
        result = get_hardware_service().open_door()
        status.update(label=result,state="error" if 'not' in  result else "complete")
        get_hardware_service().capture_camera_image()

def close_door():
    with st.status("Closing door...") as status:
        st.write("Setting output pins")
        result = get_hardware_service().close_door()
        get_hardware_service().capture_camera_image()

st.markdown(f"Door status: `{get_hardware_service().get_door_status()}`")
col1,col2,col3 = st.columns(3)
with col1:
    if st.button(label="Refresh",key="refresh"):
        get_hardware_service().capture_camera_image()
        st.rerun()
with col2:
    st.button(label="Open Door", key="open_door", on_click=open_door)
with col3:
    st.button(label="Close Door",key="close_door",on_click=close_door)

if not os.path.exists(CAMERA_IMAGE_PATH):
    get_hardware_service().capture_camera_image()

st.image(CAMERA_IMAGE_PATH)
st.markdown(f"Red eyes: `{get_hardware_service().get_red_eyes_status()}`")

