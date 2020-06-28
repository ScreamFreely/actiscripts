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

TIME_FORMAT = '%B %d, %Y %I:%M %p'

# Set initial variables for City, etc
calendar_url = 'https://www.woodburymn.gov/calendar_app/index.html#-css=css/calendar_style_woodburymn.css'

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

def getEvents(br):
    month, year = br.find_element_by_id('calendarMonthYear').text.split(' ')
    eventDays = br.find_elements_by_class_name('eventDay')
    for day in eventDays:
        dateNumber = day.find_element_by_class_name('dateNumbers').text
        if ',' in dateNumber:
            dateNumber = dateNumber.split(',')[1].strip()
        events = day.find_elements_by_class_name('foreignEventName')
        for event in events:
            d = {}
            time = day.find_element_by_class_name('meridiem').text
            d['title'] = day.find_element_by_class_name('foreignEventName').text.split(time)[1]
            dateTime = '{0} {1}, {2} {3}'.format(month, dateNumber, year, time)
            d['dateTime'] = datetime.strptime(dateTime, TIME_FORMAT)
            link = day.find_element_by_class_name('foreignEventName')
            link.click()
            sleep(3)
            br.switch_to.window(br.window_handles[1])
            d['link'] = br.current_url
            br.close()
            br.switch_to.window(br.window_handles[0])
            EVENTS.append(d)

br.get(calendar_url)
sleep(5)
getEvents(br)
br.find_element_by_class_name('nextPrevMonth').click()
sleep(3)
getEvents(br)

EVENTS = [i for n, i in enumerate(EVENTS) if i not in EVENTS[n + 1:]] 

class WoodburyEventScraper(Scraper):

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
