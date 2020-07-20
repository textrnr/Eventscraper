import requests
import datetime
from dateutil.parser import parse
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

url = config['main']['event_json']
madmin = config['main']['madmin']
auth_user = config['main']['auth_user']
auth_pass = config['main']['auth_pass']

def event_exists(name):
    events = requests.get(madmin + '/get_events', auth=(auth_user, auth_pass))
    for event in events.json():
        if name in event["event_name"]:
            return True

def get_spotlights(url):
    event_json = requests.get(url).json()
    
    for eventitem in event_json:
        name = eventitem["name"]
        start = parse(eventitem["start"])
        end = parse(eventitem["end"])
        print(f"[INFO] {name} found: {start.strftime('%H:%M:%S %d.%m.%Y')}")
        
        if event_exists(name):
            print(f"[INFO] {name} aready present, skipping...")
            continue
        print("[INFO] Creating event: " + name)
        data = {
            'event_name': name,
            'event_start_date': start.strftime("%Y-%m-%d"),
            'event_start_time': start.strftime("%H:%M"),
            'event_end_date': end.strftime("%Y-%m-%d"),
            'event_end_time': end.strftime("%H:%M"),
            'event_lure_duration': '30'
        }
        response = requests.post(madmin + '/save_event', data=data, auth=(auth_user, auth_pass))
        if response.status_code == 200:
            print("[SUCCESS] Successfully created event " + name)
        else:
            print("[ERROR] Error while creating event: " + str(response.status_code))

get_spotlights(url)