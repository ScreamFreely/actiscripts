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

DATE_FORMAT = '%m/%d/%Y'
DATE_FORMAT_2 = '%m/%d/%Y %I:%M%p'

TIME_FORMAT = '%Y-%m-%d %I:%M %p'

tz = pytz.timezone("US/Central")

calendar_url = 'https://boardmeetingmaterials.hennepin.us/#meetings'

def getDate(date):
    date_formatted = datetime.strptime(date, DATE_FORMAT)
    dow = date_formatted.weekday()
    if dow == 1:
        date = datetime.strptime(date + ' 1:30pm', DATE_FORMAT_2)
    elif dow == 3:
        date = datetime.strptime(date + ' 10:00pm', DATE_FORMAT_2)
    else:
        date = date_formatted
    return date


def getRows(br):
    source = br.page_source
    base = html.fromstring(source)
    rows = base.xpath('.//*[@id="mtgbody"]/tr')
    return rows

def getEvents(rows):
    global EVENTS
    for row in rows:
        d = {}
        cells = row.xpath('.//td')
        d['date_time'] = getDate(cells[0].xpath('.//span/text()')[0])
        d['name'] = cells[1].xpath('.//span/text()')[0]
        d['location'] = 'A-2400 Government Center 300 South 6th Street Minneapolis, MN 55487-0240'
        try:
            d['link'] = cells[2].xpath('.//span/a/@href')[0]
            ppr(d)
            EVENTS.append(d)
            print('\n\n+++\n\n')
        except Exception as e:
            d['link'] = 'https://boardmeetingmaterials.hennepin.us/#meetings'
            ppr(d)
            EVENTS.append(d)
            print('\n\n+++\n\n')


# Initiate virtual display
start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()

print("started Xvfb")

# Initiate and start the Browser
br = wd.Chrome()
# br = wd.Firefox()

br.get(calendar_url)
sleep(10)

rows = getRows(br)
getEvents(rows)

br.find_element_by_id('meetingdata_next').click()

rows = getRows(br)
getEvents(rows)


class HennepinEventScraper(Scraper):

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


                      



    
