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

DATE_FORMAT = '%B %d, %Y %I:%M %p'
DATE_FORMAT2 = '%B %d, %Y'
EVENTS = []
tz = pytz.timezone("US/Central")

# Set initial variables for City, etc
city_url = 'https://www.plymouthmn.gov/'
calendar_url = 'https://www.plymouthmn.gov/what-s-new/calendar-of-events'

os.system('pkill Xvfb')

# Initiate virtual display
start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()
print("started Xvfb")

# Initiate and start the Browser
br = wd.Chrome()
#br = wd.Firefox()

br.get(calendar_url)
sleep(5)

def get_events(br):
	global EVENTS
	ntable = br.find_elements_by_id('events_widget_294_92_34')
	cal_info = ntable[0]
	month, year = cal_info.find_element_by_class_name('calendar_title_content').text.split(' ')
	p_source = html.fromstring(br.page_source)
	events = p_source.xpath('.//*[@class="calendar_day calendar_day_with_items"]')

	for e in events:
		cal_day = e.xpath('.//text()')[0].strip()
		edivs = e.xpath('.//*[@class="calendar_item"]')
		for ed in edivs:
			d = {}
			try:
				time = ed.xpath('.//span/text()')[0]
				date_time = '{0} {1}, {2} {3}'.format(month, cal_day, year, time)
				d['date_time'] = datetime.strptime(date_time, DATE_FORMAT)
			except:
				date_time = '{0} {1}, {2}'.format(month, cal_day, year)
				d['date_time'] = datetime.strptime(date_time, DATE_FORMAT2)
			d['link'] = city_url + ed.xpath('.//*[@class="calendar_eventlink"]/@href')[0]
			d['name'] = ed.xpath('.//*[@class="calendar_eventlink"]/@title')[0]
			EVENTS.append(d)


get_events(br)
ntable = br.find_elements_by_id('events_widget_294_92_34')
cal_info = ntable[0]
cal_info.find_element_by_xpath('.//*[@class="next"]').click()
sleep(5)
get_events(br)

class PlymouthEventScraper(Scraper):

    def scrape(self):
        for c in EVENTS:
            dt = tz.localize(c['date_time'])
            try:
                e = Event(name=c['name'],
                          start_date=dt,
                          location_name='see link',
                          classification='govt')
                e.add_committee(c['name'])
                e.add_source(c['link'])
                # e.add_media_link(note="Calendar Invite",
                #                  url=c['cal_invite'],
                #                  media_type="link")
                yield e
            except Exception as e:
                print(e)
