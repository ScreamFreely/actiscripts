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


tz = pytz.timezone("US/Central")

TIME_FORMAT = '%b %d, %Y %I:%M %p'

# Set initial variables for City, etc
calendar_url = 'https://citycouncil.atlantaga.gov/other/events/public-meetings'

nope_calendar_url = 'https://www.lacity.org/government/meeting-calendars/council-and-committee-meetings'


start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()
print("started Xvfb")

# Initiate and start the Browser
# br = wd.Chrome()
br = wd.Firefox()

EVENTS = []
NEXTLINK = ''


def getEvents(url):
    global NEXTLINK
    br.get(url)
    sleep(5)
    month, year = br.find_elements_by_class_name('calendar_title_content')[0].text.split(' ')
    NEXTLINK = br.find_elements_by_class_name('calendar_nextprev')[1].find_element_by_xpath('.//a').get_attribute('href')
    days = br.find_elements_by_class_name('calendar_day_with_items')
    for day in days:
        date = '{0} {1}, {2}'.format(month, day.text, year)
        events = day.find_elements_by_class_name('calendar_item')
        for event in events:
            d = {}
            time = event.find_element_by_class_name('calendar_eventtime').text
            d['title'] = event.find_element_by_class_name('calendar_eventlink').get_attribute('title')
            d['link'] = event.find_element_by_class_name('calendar_eventlink').get_attribute('href')
            d['dateTime'] = '{0} {1}'.format(date, time)
            EVENTS.append(d)


getEvents(calendar_url)
getEvents(NEXTLINK)

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
