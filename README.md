# Event Scraper

Scrape events from https://leekduck.com/events/ and create MAD events automatically.

This script can only scrape for Spotlight Hours for now. Others like Comunity Days may follow.

## Installation/Usage

It's a normal python script, you know the drill:

1. Install requirements

`pip3 install -r requirements.txt`

2. Fill in the config

Copy the `config.ini.example` file to `config.ini` and fill out the options. If you dont use auth for MADmin, just leave the two options empty.

3. Starting

`python3 spotlighthour.py`
