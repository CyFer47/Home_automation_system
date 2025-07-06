import random

_ventilation_on = False

def get_env_status():
    humidity = random.uniform(40, 80)
    temperature = random.uniform(20, 35)
    return {
        'humidity': humidity,
        'temperature': temperature,
        'ventilation': "ON" if _ventilation_on else "OFF"
    }

def control_ventilation():
    env = get_env_status()
    global _ventilation_on
    if env['humidity'] > 70 or env['temperature'] > 30:
        _ventilation_on = True

def toggle_ventilation():
    global _ventilation_on
    _ventilation_on = not _ventilation_on
