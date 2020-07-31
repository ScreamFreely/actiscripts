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

DATE_FORMAT = '%A, %b %d, %Y'
TIME_FORMAT = '%Y-%m-%d %I:%M %p'
tz = pytz.timezone("US/Central")

# Set initial variables for City, etc
city_url = 'https://www.plymouthmn.gov/'
# council_url = 'http://www.duluthmn.gov/city-council/city-councilors'
calendar_url = 'https://www.plymouthmn.gov/what-s-new/calendar-of-events'


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
# br = wd.Chrome()
br = wd.Firefox()

br.get(calendar_url)
sleep(5)

p_source = html.fromstring(br.page_source)

events = p_source.xpath('.//*[@class="calendar_day calendar_day_with_items"]')


for e in events:
    cal_day = e.xpath('.//text()')[0].strip()
    print(cal_day)
    edivs = e.xpath('.//*[@class="calendar_item"]')
    for ed in edivs:
        d = {}
        try:
            d['time'] = ed.xpath('.//span/text()')[0]
        except:
            d['time'] = 'n/a'
        d['link'] = city_url + ed.xpath('.//*[@class="calendar_eventlink"]/@href')[0]
        d['name'] = ed.xpath('.//*[@class="calendar_eventlink"]/@title')[0]
        ppr(d)
        print('\n\n++\n\n')

ntable = br.find_elements_by_id('events_widget_294_92_34')

cal_info = ntable[0]
# cal_events = ntable[1].find_elements_by_xpath('.//tbody/tr/td')
cal_event_days = br.find_elements_by_class_name('calendar_day_with_items')


for ced in cal_event_days:
    cal_day = ced.text
    events = ced.find_elements_by_class_name('calendar_item')
    for event in events:
        d = {}
        # d['time'] = event.find_element_by_class_name('calendar_eventtime')
        d['time'] = event.find_element_by_xpath('.//span')
        d['link'] = city_url + event.find_element_by_class_name('calendar_eventlink').get_attribute('href')
        d['name'] = event.find_element_by_class_name('calendar_eventlink').get_attribute('title')
        ppr(d)



for ced in cal_event_days:
    cal_day = ced.text
    events = html.fromstring(ced.page_source)
    for event in events:
        d = {}
        # d['time'] = event.find_element_by_class_name('calendar_eventtime')
        d['time'] = event.xpath('.//span/text()')
        # d['link'] = event.find_element_by_class_name('calendar_eventlink').get_attribute('href')
        # d['name'] = event.find_element_by_class_name('calendar_eventlink').get_attribute('title')
        ppr(d)



month, year = cal_info.find_element_by_class_name('calendar_title_content').text.split(' ')
next_month = cal_info.find_element_by_xpath('.//*[@class="next"]').get_attribute('href')


br.find_element_by_class_name('fc-btn_allCalendars-button').click()

# all_entries = Select(br.find_element_by_id('showEnites'))
# all_entries.select_by_value('100')

# sleep(5)

# cal = br.find_element_by_xpath('//*[@class="col-md-12 form-group"]')

# dates = cal.find_elements_by_class_name('ng-scope')

eventDates = []

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

