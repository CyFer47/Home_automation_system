import csv
import os
from datetime import datetime, timedelta
from utils.controller import get_water_status, toggle_valve

WATER_HISTORY = 'data/water_history.csv'
ABNORMAL_WATER = 'data/abnormal_water.csv'

def log_water_flow():
    now = datetime.now()
    flow = get_water_status()['flow_rate']
    with open(WATER_HISTORY, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now.strftime('%Y-%m-%d %H:%M:%S'), flow])

def get_water_history():
    if not os.path.exists(WATER_HISTORY):
        return []
    with open(WATER_HISTORY) as f:
        # Return last 24 entries for hourly intervals (24 hours)
        return list(csv.reader(f))[-24:]

def get_hourly_consumption():
    # Calculate hourly consumption, compare with previous 3 hours
    # If abnormal, log and cut off water
    pass

def check_abnormal_consumption():
    if not os.path.exists(ABNORMAL_WATER):
        return []
    with open(ABNORMAL_WATER) as f:
        return list(csv.reader(f))
