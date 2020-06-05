import re, os
from datetime import datetime

from pprint import pprint as ppr

from time import sleep
from pprint import pprint as ppr
from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException

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
calendar_url = 'https://duluthmn.gov/event-calendar/'

DATE_FORMAT = '%b %d, %Y %I:%M%p'
ALT_DATE_FORMAT = '%b %d, %Y'

# Setting up routine processes
def get_base(site):
    s = requests.get(site)
    b = html.fromstring(s.text)
    return b

# Initiate virtual display
start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()
print("started Xvfb")

# Initiate and start the Browser
br = wd.Chrome()

# Go to specified URL
br.get(calendar_url)
sleep(3)
collectedRows = []
# Changing to List style view
br.find_elements_by_xpath('.//*/a[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_btnCalendarViewList"]')[0].click()
# Get the rows in the table of events 
def getRows(br):
    rows = br.find_elements_by_xpath('.//*/div[@id="pnlCalendar"]/div/div/table/tbody/tr/td[@class="tblListCalendarEventCell"]/span')
    numOfRows = len(rows)-1
    return rows, numOfRows


# Set a variable to the number of rows in the table
# numOfRows = len(rows)-1
# print(numOfRows)

# Create empty list to collect event data


# PROCESS FOR FOLLOWING FOR LOOP
"""
0) cycle through a range of integers equal to numOfRows
1) create new dictionary
2) Refresh the rows variable
3) Set 'row' equal to the next row
4) Add 'title' to our dictionary
5) 'TRY' to get more event info
6) 'Click' on the row in question
7) Get Event date
8) Event Info
9) Close the pop-up window
10) Append new dictionary to list collectedRows
11) if that doesn't work --- let us know why
12) if a pop-up failed to close, try closing it
"""

def getInfo(rows, numOfRows, br):
    for n in range(0,numOfRows):
        print("\n\n ++++++ \n\n")
        nR = {}
        rows = br.find_elements_by_xpath('.//*/div[@id="pnlCalendar"]/div/div/table/tbody/tr/td[@class="tblListCalendarEventCell"]/span')
        row = rows[n]
        nR['title'] = row.text
        row.click()
        sleep(3)
        dateInfo = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]/table/tbody/tr/td')[0].text
        dateInfo = dateInfo.split("\n")
        dateTime = dateInfo[1] + ' '+ dateInfo[2]
        dateTime = dateTime.split('-')[0].strip()
        try:
            nR['dateTime'] = datetime.strptime(dateTime, DATE_FORMAT)
        except:
            nR['dateTime'] = datetime.strptime(dateTime, ALT_DATE_FORMAT)
        moreInfo = dateInfo[3:-7]
        n = 0
        loc = False
        site = False
        nR['moreInfo'] = []
        nR['location'] = []
        for mi in moreInfo:
            mi = mi.strip()
            if site == True:
                nR['website'] = mi
                continue
            elif mi == 'Location:':
                loc = True
                continue
            elif loc == False and not mi == 'Location:':
                nR['moreInfo'].append(mi)
                continue
            elif mi == 'Website:':
                loc = False
                site = True
                continue
            elif loc == True:
                nR['location'].append(mi)
                continue
            else:
                print('oops')
        nR['location'] = (' ').join(nR['location'])
        nR['moreInfo'] = ('\n').join(nR['moreInfo'])
        if len(nR['location']) < 1:
            nR['location'] = 'n/a'
        # for di in dateInfo:
        #   print(di)
        #   print()
        br.find_elements_by_xpath('.//*/button[@title="Close"]')[0].click()
        sleep(3)
        collectedRows.append(nR)



for x in range(0,3):
    rows, numOfRows = getRows(br)
    getInfo(rows, numOfRows, br)
    nextBtn = br.find_elements_by_xpath('.//*/i[@class="fas fa-angle-double-right"]')[0]
    nextBtn.click()
    print('\n\n New New coming soon \n\n')
    print(len(collectedRows))
    sleep(3)


os.system('pkill Xvfb')





class DuluthEventScraper(Scraper):

    def scrape(self):
        for c in collectedRows:
            print(c)
            dt = tz.localize(c['dateTime'])
            e = Event(name=c['title'],
                      start_date=dt,
                      location_name=c['location'],
                      classification='govt')
            # e.add_committee(c['CommitteeName']
            if 'website' in c:
                e.add_source(c['website'])
                # e.add_media_link(note="Event link",
                #              url=c['website'],
                #              media_type="link")
            else:
                e.add_source(calendar_url)
                # e.add_media_link(note="Calendar link",
                #              url=calendar_url,
                #              media_type="link")
            
            # if c['MarkedAgendaPublished'] == True:
            #     event_url = "{0}{1}/{2}".format(AGENDA_BASE_URL, c['Abbreviation'], c['AgendaId'])
            #     e.add_media_link(note="Agenda",
            #                      url=event_url,
            #                      media_type="link")
            yield e
