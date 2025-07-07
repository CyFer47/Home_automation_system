# utils/ventilation.py

import board
import adafruit_dht

_ventilation_on = False
dhtDevice = adafruit_dht.DHT11(board.D4)

def get_env_status():
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        return {
            'temperature': temperature,
            'humidity': humidity,
            'ventilation': "ON" if _ventilation_on else "OFF"
        }
    except RuntimeError:
        return {
            'temperature': None,
            'humidity': None,
            'ventilation': "ON" if _ventilation_on else "OFF"
        }

def control_ventilation():
    global _ventilation_on
    env = get_env_status()
    if (env['humidity'] is not None and env['humidity'] > 70) or (env['temperature'] is not None and env['temperature'] > 30):
        _ventilation_on = True
    else:
        _ventilation_on = False

def toggle_ventilation():
    global _ventilation_on
    _ventilation_on = not _ventilation_on
