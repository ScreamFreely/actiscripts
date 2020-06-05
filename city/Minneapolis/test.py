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
city_url = 'http://www.duluthmn.gov'
council_url = 'http://www.duluthmn.gov/city-council/city-councilors'
calendar_url = 'https://lims.minneapolismn.gov/Calendar/citycouncil/upcoming'


def convert_date(date):
    new_date = datetime.strftime(date, DATE_FORMAT)
    return new_date.replace(' ', '%20')


# Setting up routine processes
def get_base(site):
    s = requests.get(site)
    b = html.fromstring(s.text)
    return b




# Initiate virtual display
# start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
# xvfb = Xvfb()

# Start the virtual display

# os.system(start_cmd)
# xvfb.start()

print("started Xvfb")

# Initiate and start the Browser
br = wd.Firefox()

br.get(calendar_url)
sleep(10)

br.find_element_by_class_name('fc-btn_allCalendars-button').click()

all_entries = Select(br.find_element_by_id('showEnites'))
all_entries.select_by_value('100')

sleep(5)

cal = br.find_element_by_xpath('//*[@class="col-md-12 form-group"]')

dates = cal.find_elements_by_class_name('ng-scope')

DATE_FORMAT = '%A, %b %d, %Y'
TIME_FORMAT = '%Y-%m-%d %I:%M %p'

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

def processSpan(div):
    links = div.find_elements_by_tag_name('a')
    spans = div.find_elements_by_tag_name('span')
    deets = {}
    if len(links) == 1:
        name = div.find_elements_by_tag_name('span')[0].text
        deets['xport'] = links[0].get_attribute('href')
        deets['href'] = None
    else:
        deets['href'] = links[0].get_attribute('href')
        deets['xport'] = links[1].get_attribute('href')
        name = links[0].text 
    deets['name'] = name.replace('This link open a new window', '').replace('\n', '')
    return deets




for item in realDates[:5]:
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
                e['room'] = names[1].strip()
                e['location'] = names[2].strip()
            elif len(names) == 2:
                e['name'] = names[0]
                e['location'] = names[1].strip()
                e['room'] = 'n/a'
            ppr(e)
            print('\n ^^^ new event ^^^ \n\n')
        except:
            continue
    print('\n\n Change Date \n\n')
