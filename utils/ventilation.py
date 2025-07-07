import board
import adafruit_dht
import time

_ventilation_on = False
dhtDevice = adafruit_dht.DHT11(board.D4)
_last_read = 0
_last_temp = None
_last_hum = None

def get_env_status():
    global _last_read, _last_temp, _last_hum
    now = time.time()
    if now - _last_read > 2:
        try:
            _last_temp = dhtDevice.temperature
            _last_hum = dhtDevice.humidity
        except RuntimeError as e:
            print("DHT11 read error:", e)
        _last_read = now
    return {
        'temperature': _last_temp,
        'humidity': _last_hum,
        'ventilation': "ON" if _ventilation_on else "OFF"
    }

def toggle_ventilation():
    global _ventilation_on
    _ventilation_on = not _ventilation_on
