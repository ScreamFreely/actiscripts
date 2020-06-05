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

# Set initial variables for City, etc
calendar_url = 'https://lims.minneapolismn.gov/Calendar/citycouncil/upcoming'


def processSpan(div):
    links = div.find_elements_by_tag_name('a')
    spans = div.find_elements_by_tag_name('span')
    deets = {}
    if len(links) == 1:
        name = div.find_elements_by_tag_name('span')[0].text
        deets['xport'] = links[0].get_attribute('href')
        deets['href'] = 'https://lims.minneapolismn.gov/Calendar/citycouncil/upcoming'
    else:
        deets['href'] = links[0].get_attribute('href')
        deets['xport'] = links[1].get_attribute('href')
        name = links[0].text 
    deets['name'] = name.replace('This link open a new window', '').replace('\n', '')
    return deets


# Initiate virtual display
start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()
print("started Xvfb")

# Initiate and start the Browser
br = wd.Chrome()

br.get(calendar_url)
sleep(10)

br.find_element_by_class_name('fc-btn_allCalendars-button').click()

all_entries = Select(br.find_element_by_id('showEnites'))
all_entries.select_by_value('25')

sleep(5)

cal = br.find_element_by_xpath('//*[@class="col-md-12 form-group"]')

dates = cal.find_elements_by_class_name('ng-scope')

DATE_FORMAT = '%A, %b %d, %Y'
TIME_FORMAT = '%Y-%m-%d %I:%M %p'
EVENTS = []

realDates = []

for date in dates:
    date.find_elements_by_xpath('//div/div/span[@class="ng-binding"]')[0]
    check = date.text.split('\n')[0]
    print(check)
    try:
        d = {}
        d['datestamp'] = datetime.strptime(check, DATE_FORMAT)
        d['date'] = date
        realDates.append(d)
    except:
        continue


for item in realDates:
    nds = str(item['datestamp']).split(' ')[0]
    date = item['date']
    events = date.find_elements_by_class_name('row')
    for event in events[:3]:
        divs = event.find_elements_by_tag_name('div')
        time = divs[0].text
        try:
            e = {}
            ndt = nds + ' ' + time
            e['date_time'] = datetime.strptime(ndt, TIME_FORMAT)
            print(ndt)
            deets = processSpan(divs[2])
            e['link'] = deets['href']
            e['cal_invite'] = deets['xport']
            names = deets['name'].split(',')
            if len(names) == 3:
                e['name'] = names[0]
                e['location'] = names[1].strip() + ' ' + names[2].strip()
            elif len(names) == 2:
                e['name'] = names[0]
                e['location'] = names[1].strip()
            EVENTS.append(e)
        except:
            continue


class MinneapolisEventScraper(Scraper):

    def scrape(self):
        for c in EVENTS:
            dt = tz.localize(c['date_time'])
            try:
                e = Event(name=c['name'],
                          start_date=dt,
                          location_name=c['location'],
                          classification='govt')
                e.add_committee(c['name'])
                e.add_source(c['link'])
                # e.add_media_link(note="Calendar Invite",
                #                  url=c['cal_invite'],
                #                  media_type="link")
                yield e
            except Exception as e:
                print(e)


                      



    
