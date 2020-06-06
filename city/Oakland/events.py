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

tz = pytz.timezone("US/Central")

# Set initial variables for City, etc
calendar_url = 'https://oakland.legistar.com/calendar.aspx'

start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()
print("started Xvfb")

# Initiate and start the Browser
# br = wd.Chrome()
br = wd.Firefox()

br.get(calendar_url)
sleep(10)

def getRows(br):
	table = br.find_element_by_class_name('rgMasterTable')
	rows = table.find_elements_by_xpath('.//tbody/tr')
	return rows

def processRows(rows):
	for row in rows:
		cells = row.find_elements_by_xpath('.//td')
		d= {}
		d['title'] = cells[0].text
		d['location'] = cells[4].text.replace('\n', '')
		date = cells[1].text
		time = cells[3].find_element_by_xpath('.//span').text
		d['datetime'] = date + ' ' + time
		d['details'] = cells[5].find_element_by_xpath('.//a').text
		d['agenda'] = cells[5].find_element_by_xpath('.//a').text
		d['detailsLink'] = cells[5].find_element_by_xpath('.//a').get_attribute('href')
		d['agendaLink'] = cells[5].find_element_by_xpath('.//a').get_attribute('href')
		EVENTS.append(d)

rows = getRows(br)
processRows(rows)

next_week = br.find_element_by_id('ctl00_ContentPlaceHolder1_lstYears_Input')
next_week.send_keys('N')
next_week.submit()

rows = getRows(br)
processRows(rows)

EVENTS = [i for n, i in enumerate(EVENTS) if i not in EVENTS[n + 1:]]


class OaklandEventScraper(Scraper):

    def scrape(self):
        # needs to be implemented
        pass
