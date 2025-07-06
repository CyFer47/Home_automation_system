# utils/controller.py

import RPi.GPIO as GPIO

# GPIO pin assignments (adjust as needed)
RELAY_LIGHT = 17
RELAY_FAN = 27
RELAY_VALVE = 22

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_LIGHT, GPIO.OUT)
GPIO.setup(RELAY_FAN, GPIO.OUT)
GPIO.setup(RELAY_VALVE, GPIO.OUT)

# Initial states: relays OFF (HIGH)
GPIO.output(RELAY_LIGHT, GPIO.HIGH)
GPIO.output(RELAY_FAN, GPIO.HIGH)
GPIO.output(RELAY_VALVE, GPIO.HIGH)

_light_status = False
_fan_status = False
_valve_status = False
_light_brightness = 70  # default brightness in %

def toggle_light():
    global _light_status
    _light_status = not _light_status
    GPIO.output(RELAY_LIGHT, GPIO.LOW if _light_status else GPIO.HIGH)

def toggle_fan():
    global _fan_status
    _fan_status = not _fan_status
    GPIO.output(RELAY_FAN, GPIO.LOW if _fan_status else GPIO.HIGH)

def toggle_valve():
    global _valve_status
    _valve_status = not _valve_status
    GPIO.output(RELAY_VALVE, GPIO.LOW if _valve_status else GPIO.HIGH)

def set_brightness(level):
    global _light_brightness
    # Implement PWM as needed for real hardware
    _light_brightness = int(level)

def get_status():
    return {
        'light': "ON" if _light_status else "OFF",
        'fan': "ON" if _fan_status else "OFF",
        'valve': "OPEN" if _valve_status else "CLOSED",
        'brightness': _light_brightness
    }

def get_light_status():
    return "ON" if _light_status else "OFF"

def get_fan_status():
    return "ON" if _fan_status else "OFF"

def get_valve_status():
    return "OPEN" if _valve_status else "CLOSED"

def get_water_status():
    # Example flow rate in liters per minute
    flow_rate = 12.5
    return {
        'flow_rate': flow_rate,
        'valve_status': get_valve_status()
    }
