import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse
import json
import configparser

events = list()

def get_spotlights(url):
    content = requests.get(url).text
    
    soup = BeautifulSoup(content, "html.parser")
    for eventitem in soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['event-item-link']):
        if eventitem["href"].startswith("/events/pokemonspotlighthour"):
            name = eventitem.find('h2').get_text()
            dt = parse(eventitem.find('div', {'class': 'event-countdown'})["data-countdown"])
            print(f"[INFO] {name} found: {dt.strftime('%H:%M:%S %d.%m.%Y')}")
            
            # Generate a list of all events
            event = {"name": name, "start": str(dt.strftime("%Y-%m-%d %H:%M")), "end": str(dt + datetime.timedelta(hours=1)), "local_times": True}
            events.append(event)

get_spotlights("https://leekduck.com/events/")
with open('mad-events.json', 'w') as f:
    json.dump(events, f, indent =2)
    print("writing json")