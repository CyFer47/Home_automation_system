light_state = False
fan_state = False

def toggle_light():
    global light_state
    light_state = not light_state

def toggle_fan():
    global fan_state
    fan_state = not fan_state

def get_status():
    return {
        'light': 'ON' if light_state else 'OFF',
        'fan': 'ON' if fan_state else 'OFF'
    }
