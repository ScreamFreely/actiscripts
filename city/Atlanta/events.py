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


tz = pytz.timezone("US/Eastern")

TIME_FORMAT = '%B %d, %Y %I:%M %p'
TIME_FORMAT2 = '%B %d, %Y'

# Set initial variables for City, etc
calendar_url = 'https://citycouncil.atlantaga.gov/other/events/public-meetings'

base_url = 'https://citycouncil.atlantaga.gov'

os.system('pkill Xvfb')
start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()
print("started Xvfb")

# Initiate and start the Browser
br = wd.Chrome()
# br = wd.Firefox()

EVENTS = []
NEXTLINK = ''

def getSite(url):
    br.get(url)
    sleep(5)
    s = br.page_source
    b = html.fromstring(s)
    return b

def getEvents(url):
    global NEXTLINK
    b = getSite(url)
    month, year = b.xpath('.//*/td[@class="calendar_title_content"]/h2/text()')[0].strip().split(' ')
    NEXTLINK = b.xpath('.//*/td[@class="calendar_nextprev"]/a/@href')[1]
    days = b.xpath('.//*/td[@class="calendar_day calendar_day_with_items"]')
    for day in days:
        date = '{0} {1}, {2}'.format(month, day.xpath('.//text()')[0].strip(), year)
        events = day.xpath('.//div/div[@class="calendar_item"]')
        for event in events:
            d = {}
            d['title'] = event.xpath('.//a/text()')[0]
            d['link'] = event.xpath('..//a/@href')[0]
            try:
                time = event.xpath('.//span/text()')[0]
                dateTime = '{0} {1}'.format(date, time)
                d['datetime'] = datetime.strptime(dateTime, TIME_FORMAT)
            except Exception as e:
                d['datetime'] = datetime.strptime(date, TIME_FORMAT2)
            EVENTS.append(d)


getEvents(calendar_url)
getEvents(base_url + NEXTLINK)

EVENTS = [i for n, i in enumerate(EVENTS) if i not in EVENTS[n + 1:]] 

class AtlantaEventScraper(Scraper):

    def scrape(self):
        for c in EVENTS:
            dt = tz.localize(c['dateTime'])
            e = Event(name=c['title'],
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
