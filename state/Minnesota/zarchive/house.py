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
# br = wd.Firefox()
br.get('https://www.leg.state.mn.us/cal?type=all')
sleep(3)
base = html.fromstring(br.page_source)
xvfb.stop()

os.system("pkill Xvfb")

house_base = base.xpath('.//div[@class="card border-dark house_item cal_item ml-lg-3"]')

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


class MNHouseScraper(Scraper):

    def scrape(self):
        for c in house_base:
            m = {}
            try:
                header = c.xpath('.//div[@class="card-header bg-house text-white"]')[0]
            except:
                print('\n\n ++++ \n\n')
                print(type(c))
                continue 
            print("header", header)
            info_div = c.xpath('.//div[@class="card-body"]/table/tbody/tr')
            print("info_div", info_div)
            m['notice'] = header.xpath('.//span/span[@class="cal_special"]/text()')
            links = header.xpath('.//h3/a/@href')  
            print("links", links)           
            if len(links) > 0:
                m['cmt'] = header.xpath('.//h3/a/text()')[0]
                m['link'] = header.xpath('.//h3/a/@href')[0]
                if len(header.xpath('.//h3/text()')) > 0:
                    m['title'] = header.xpath('.//h3/text()')[0]  
                else:
                    m['title'] = header.xpath('.//h3/a/text()')[0]

            else:
                m['title'] = header.xpath('.//h3/text()')[0]
                m['link'] = None
            info_div = c.xpath('.//div[@class="card-body"]')[0]
            if len(info_div) == 0:
                pass
            # else:
            #     info_div = info_div[0]
            if len(info_div) > 0:
                info_list = info_div.xpath('.//div/b/text()')
                info_text = info_div.xpath('.//div/text()')
                info_links = info_div.xpath('.//div/*/@href')
                print("info links: ", info_links)
                print("info text: ", info_text)
                if info_list[0].startswith('Room:'):
                    m['room'] = info_text[0]
                else:
                    m['room'] = 'n/a'
                # info_list = [x.replace('\n', '').strip() for x in info_list]
                # info_list = [x for x in info_list if len(x) > 0]
                # print('Info list: ', info_list)
                # if info_list[0].startswith('Room:'):
                #     m['room'] = info_list[1]
                # else:
                #     m['room'] = 'n/a'
                # if len(info_list) > 2:
                #     if info_list[2].startswith('Chair:'):
                #         chair = info_list[3]
                #         if ',' in chair:
                #             chairs = chair.replace('\xa0', '').split(',')
                #             nchairs = []
                #             for chair in chairs:
                #                 if chair.startswith('Rep.') or chair.startswith('Sen.'):
                #                     cname = pull_middle_name(chair[4:])
                #                     nchairs.append(cname.strip())
                #             m['chair'] = nchairs
                #         elif chair.startswith('Rep.') or chair.startswith('Sen.'):
                #             cname = pull_middle_name(chair[4:].strip())
                #             m['chair'] = [cname.strip()]
                # else:
                #     m['chair'] = None
  

            # bill_rows = c.xpath(('.//*/table[@class="cal_bills"]/tbody/tr'))
            # print('Bills: ', bill_rows)
            # bills = []
            # for brs in bill_rows:
            #     cells = brs.xpath('.//td')
            #     if len(cells) == 3:
            #         b = {}
            #         b['bill'] = cells[0].xpath('.//text()')[0]
            #         b['author'] = cells[1].xpath('./text()')[0]
            #         b['summary'] = cells[2].xpath('./text()')[0]
            #         bills.append(b)
            if len(m['notice']) > 0:
                m['notice'] = m['notice'][0]
            else:
                m['notice'] = 'N/A'
            date = header.xpath('.//b/text()')
            if len(date) < 1:
                print('\n\n\n\n NO DATE')
                continue
            m['date'] = datetime.datetime.strptime(date[0], format1)

            if 'House Meets in Session' in m['title']:
                m['room'] = 'State leg'
                m['cmt'] = 'Minnesota House of Representatives in Session'
                m['chair'] = None
                m['link'] = 'https://www.leg.state.mn.us/cal?type=all'
            m['room'] = m['room'] + ' House, State Legislature'
            event = Event(name=m['title'],
                          start_date=tz.localize(m['date']),
                          location_name=m['room'],
                          classification='govt' 
            )
            # if len(bills) > 0:
            #     for bill in bills:
            #         nbill = event.add_agenda_item(description=bill['summary'])
            #         nbill.add_bill(bill['bill'].replace('HF', 'HF '))
            if len(m['notice']) > 0:
                pass
            event.add_committee(m['cmt'])
            if m['link'] is not None:
                event.add_source(m['link'])
            if 'chair' in m:
                for chair in m['chair']:
                   event.add_person(name=chair, note="Chair")
            yield event
