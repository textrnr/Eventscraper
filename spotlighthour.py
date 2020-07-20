import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

url = 'https://leekduck.com/events/'
madmin = config['main']['madmin']
auth_user = config['main']['auth_user']
auth_pass = config['main']['auth_pass']

def event_exists(name):
    events = requests.get(madmin + '/get_events', auth=(auth_user, auth_pass))
    for event in events.json():
        if name in event["event_name"]:
            return True


def get_spotlights(url):
    content = requests.get(url).text
    
    soup = BeautifulSoup(content, "html.parser")
    for eventitem in soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['event-item-link']):
        if eventitem["href"].startswith("/events/pokemonspotlighthour"):
            name = eventitem.find('h2').get_text()
            dt = parse(eventitem.find('div', {'class': 'event-countdown'})["data-countdown"])
            print(f"[INFO] {name} found: {dt.strftime('%H:%M:%S %d.%m.%Y')}")
            
            if event_exists(name):
                print(f"[INFO] {name} aready present, skipping...")
                continue
            print("[INFO] Creating event: " + name)
            end = dt + datetime.timedelta(hours=1)
            data = {
                'event_name': name,
                'event_start_date': dt.strftime("%Y-%m-%d"),
                'event_start_time': dt.strftime("%H:%M"),
                'event_end_date': dt.strftime("%Y-%m-%d"),
                'event_end_time': end.strftime("%H:%M"),
                'event_lure_duration': '30'
            }
            response = requests.post(madmin + '/save_event', data=data, auth=(auth_user, auth_pass))
            if response.status_code == 200:
                print("[SUCCESS] Successfully created event " + name)
            else:
                print("[ERROR] Error while creating event: " + str(response.status_code))

get_spotlights(url)