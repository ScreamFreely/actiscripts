import re, os
from datetime import datetime

from pprint import pprint as ppr
import json
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

# Set initial variables for City, etc
calendar_url = ['https://www.lacity.org/government/meeting-calendars/city-council-meetingsagendas',
 				'https://www.lacity.org/government/meeting-calendars/city-council-committee-meetingsagendas',
 				'https://www.lacity.org/government/meeting-calendars/board-meetings',
 				'https://www.lacity.org/government/meeting-calendars/neighborhood-council-meetings']

nope_calendar_url = 'https://www.lacity.org/government/meeting-calendars/council-and-committee-meetings'


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
TIME_FORMAT = '%b %d, %I:%M %p'


def getEvents(cu):
	br.get(cu)
	sleep(10)
	bases = br.find_elements_by_class_name('calendar-button')

	for e in bases:
		try:
			d = {}
			d['title'] = e.find_element_by_class_name('event-panel-title').text
			dt = e.find_element_by_class_name('event-panel-datetime').text
			d['datetime'] = datetime.strptime(dt, TIME_FORMAT)
			e.click()
			sleep(3)
			br.switch_to.window(br.window_handles[1])
			d['link'] = br.current_url
			br.close()
			br.switch_to.window(br.window_handles[0])
			EVENTS.append(d)
		except Exception as e:
			pass


for cal in calendar_url:
	getEvents(cal)


# EVENTS = [i for n, i in enumerate(EVENTS) if i not in EVENTS[n + 1:]] 


ppr(EVENTS)

class LosangelesEventScraper(Scraper):

    def scrape(self):
        for c in EVENTS:
            dt = tz.localize(c['datetime'])
            try:
                e = Event(name=c['title'],
                          start_date=dt,
                          location_name='see link',
                          classification='govt')
                # e.add_committee(c['name'])
                e.add_source(c['link'])
                # e.add_media_link(note="Calendar Invite",
                #                  url=c['cal_invite'],
                #                  media_type="link")
                yield e
            except Exception as e:
                print(e)
