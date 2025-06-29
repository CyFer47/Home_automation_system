# utils/controller.py

# Simulated device states
_light_status = False
_fan_status = False
_valve_status = False
_light_brightness = 70  # default brightness in %

def toggle_light():
    global _light_status
    _light_status = not _light_status
    # TODO: Add hardware control to toggle the light (e.g., GPIO, PWM)

def toggle_fan():
    global _fan_status
    _fan_status = not _fan_status
    # TODO: Add hardware control to toggle the fan

def toggle_valve():
    global _valve_status
    _valve_status = not _valve_status
    # TODO: Add hardware control to open/close valve (e.g., relay control)

def set_brightness(level):
    global _light_brightness
    if level in [25, 50, 75, 100]:
        _light_brightness = level
        # TODO: Implement PWM or DAC control to set brightness

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

# Simulated water flow sensor status
def get_water_status():
    # Example flow rate in liters per minute
    flow_rate = 12.5  
    return {
        'flow_rate': flow_rate,
        'valve_status': get_valve_status()
    }
