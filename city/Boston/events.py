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


EVENTS = []
TIME_FORMAT = '%m/%d/%Y %I:%M %p'

tz = pytz.timezone("US/Eastern")

# Set initial variables for City, etc
base_url = 'https://www.boston.gov/public-notices'
calendar_url = 'https://www.boston.gov/public-notices'

start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()
print("started Xvfb")

# Initiate and start the Browser
# br = wd.Chrome()
br = wd.Firefox()

def getSite(url):
	br.get(url)
	sleep(10)
	root = br.page_source
	s = html.fromstring(root)
	return s 

def getEvents(s):
	events = s.xpath('.//*/div[@class="g g--m0 n-li"]')
	for e in events:
		d = {}
		d['title'] = e.xpath('.//*/div[@class="n-li-t"]/a/text()')[0]
		d['titleLink'] = base_url + e.xpath('.//*/div[@class="n-li-t"]/a/@href')[0]
		info = e.xpath('.//*/li[@class="dl-i"]')
		d['when'] = info[0].xpath('.//span[@class="dl-d"]/text()')[0].strip()
		d['where'] = []
		d['locality'] = ''
		where = [info[1].xpath('.//*/div[@class="name-block"]/text()')[0].strip(), 
				info[1].xpath('.//*/div[@class="thoroughfare"]/text()')[0].strip(),
				info[1].xpath('.//*/div[@class="premise"]/text()')[0].strip()]
		for w in where:
			if len(w) > 0:
				d['where'].append(w)
		if len(d['where']) > 1:
			d['where'] = ' '.join(d['where'])
		else:
			d['where'] = d['where'][0]
		locality = [info[1].xpath('.//*/span[@class="locality"]/text()')[0].strip(),
					info[1].xpath('.//*/span[@class="state"]/text()')[0].strip(),
					info[1].xpath('.//*/span[@class="postal-code"]/text()')[0].strip(),]
		for l in locality:
			if len(l) > 0:
				d['locality'] = d['locality'] + ' ' + l
				d['locality'] = d['locality'].strip()
		EVENTS.append(d)


nextBtn = 'start'

while len(nextBtn) > 0:
	ns = getSite(calendar_url)
	getEvents(ns)
	try:
		nextBtn = ns.xpath('.//*/li[@class="pager__item pager__item--next pager-item"]/a/@href')[0]
		print(nextBtn)
		calendar_url = calendar_url + nextBtn
	except Exception as e:
		print(e)
		nextBtn = ''
		pass


class BostonEventScraper(Scraper):

    def scrape(self):
        for c in EVENTS:
            dt = tz.localize(c['datetime'])
            try:
                e = Event(name=c['title'],
                          start_date=dt,
                          location_name=c['where'],
                          classification='govt')
                # e.add_committee(c['name'])
                try:
                	e.add_source(c['titleLink'])
                except:
                	e.add_source(base_url)
                # e.add_media_link(note="Calendar Invite",
                #                  url=c['cal_invite'],
                #                  media_type="link")
                yield e
            except Exception as e:
                print(e)
