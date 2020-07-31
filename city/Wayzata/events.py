import re, os
from datetime import datetime

from pprint import pprint as ppr

from time import sleep
from pprint import pprint as ppr
from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from xvfbwrapper import Xvfb

import requests
from lxml import html

from pupa.scrape import Scraper
from pupa.scrape import Event

import pytz

DATE_FORMAT = '%B %d, %Y'
DATE_FORMAT2 = '%B %d, %Y'
EVENTS = []
tz = pytz.timezone("US/Central")

# Set initial variables for City, etc
city_url = 'https://www.wayzata.org'
calendar_url = 'https://www.wayzata.org/calendar.aspx'

os.system('pkill Xvfb')

# # Initiate virtual display
# start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
# xvfb = Xvfb()

# # Start the virtual display
# os.system(start_cmd)
# xvfb.start()
# print("started Xvfb")

# Initiate and start the Browser
br = wd.Chrome()
#br = wd.Firefox()

br.get(calendar_url)
sleep(5)

page_source = html.fromstring(br.page_source)

events = ps.xpath('.//*[@class="section featured"]/ol/li')

for event in events:
    d = {}
    d['link'] = city_url + event.xpath('.//a/@href')[0]
    d['name'] = event.xpath('.//h4/text()')[0]
    date_time = event.xpath('.//p/text()')[0].strip().replace('\xa0', ' ')
    d['date_time'] = datetime.strptime(date_time, DATE_FORMAT)
    EVENTS.append(d)


class WayzataEventScraper(Scraper):

    def scrape(self):
        for c in EVENTS:
            dt = tz.localize(c['date_time'])
            e = Event(name=c['name'],
                      start_date=dt,
                      location_name='see link',
                      classification='govt')
            # e.add_committee(c['CommitteeName'])
            e.add_source(c['link'])
            # e.add_media_link(note="Event link",
            #                  url=c['link'],
            #                  media_type="link")
            # if c['MarkedAgendaPublished'] == True:
            #     event_url = "{0}{1}/{2}".format(AGENDA_BASE_URL, c['Abbreviation'], c['AgendaId'])
            #     e.add_media_link(note="Agenda",
            #                      url=event_url,
            #                      media_type="link")
            yield e
