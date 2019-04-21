from pupa.scrape import Scraper
from pupa.scrape import Event

import re, os
import datetime

from time import sleep
from pprint import pprint as ppr
from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException

import requests
from lxml import html
from lxml.etree import tostring

import pytz

from xvfbwrapper import Xvfb

tz = pytz.timezone("US/Central")

start_cmd = "Xvfb :93 && export DISPLAY=:93 &"
xvfb = Xvfb()

os.system(start_cmd)
xvfb.start()

br = wd.Chrome()
br.get('https://www.leg.state.mn.us/cal?type=all')
sleep(30)
base = html.fromstring(br.page_source)
xvfb.stop()

os.system("pkill Xvfb")
#from html2text import html2text


house_base = base.xpath('.//div[@class="card border-dark senate_item cal_item ml-lg-3"]')

print(house_base)

format1 = "%A, %B %d, %Y %I:%M %p"
format2 = "%A %B %d, %Y - "
format3 = "%m/%d/%y"

def pull_middle_name(name):
    stopwords = ['Jr.', 'Sr.', 'III']
    name = name.strip().split(' ')
    print('NAME: ', name)
    if not any(sw in name for sw in stopwords) and len(name) == 3:
        name.pop(1)
        name = ' '.join(name)
    else:
        name = ' '.join(name)
    print('NAME: ', name)
    return name


for c in house_base:
    m = {}
    header = c.xpath('.//div[@class="card-header bg-senate text-white"]')[0]
    print("header", header)
    info_div = c.xpath('.//div[@class="card-body"]/table/tbody/tr')
    print("info_div", info_div)
    m['notice'] = header.xpath('.//span/span[@class="cal_special"]/text()')
    links = header.xpath('.//h3/a/@href')  
    print("links", links)          
    if len(links) > 0:
        m['cmt'] = header.xpath('.//h3/a/text()')[0]
        m['link'] = header.xpath('.//h3/a/@href')[0] 
        m['title'] = header.xpath('.//h3/a/text()')[0]     
    else:
        m['title'] = header.xpath('.//h3/text()')
        m['link'] = None
    # date = header.xpath('.//b/text()')
    # if len(date) < 1:
    #     print('\n\n\n\n NO DATE')
    #     continue
    # m['date'] = datetime.datetime.strptime(date[0], format1)


    if len(info_div) > 0:
        info_div_1 = info_div[0]
        info_div_2 = info_div[1]
        try:
            m['chair'] = info_div_1.xpath('.//i/a/text()')[0]
        except:
            pass
        try:
            header_text = info_div_1.xpath('.//text()')
            for ht in header_text:
                if ht.startswith("Room"):
                    m['room'] = ht
        except:
            pass
    if len(m['notice']) > 0:
        m['notice'] = m['notice'][0]
        m['title']  = m['title'] + ' ' + m['notice']
    else:
        m['notice'] = 'N/A'
    date = header.xpath('.//span[@class="cal_revision"]/text()')
    if len(date) < 1:
        print('\n\n\n\n NO DATE')
        ppr(m)
        continue
    if 'or' in date[0]:
        date[0] = date[0].split('or')[0]
    m['date'] = datetime.datetime.strptime(date[0].replace('\xa0', ''), format1)
    if not 'room' in m.keys():
        print('no room number')
        m['room'] = 'Senate in session'

    ppr(m)
    print("\n\n\n+++++++\n\n\n")

    # event = Event(name=m['title'],
    #               start_date=tz.localize(m['date']),
    #               location_name=m['room'],
    #               classification='govt' 
    # )

    # if len(m['notice']) > 0:
    #     pass
    # event.add_committee(m['title'])
    # event.add_source(m['link'])
    # for chair in m['chair']:
    #     event.add_person(name=chair, note="Chair")