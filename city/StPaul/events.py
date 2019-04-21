from pupa.scrape import Scraper
from pupa.scrape import Event

import requests
from datetime import datetime
from pprint import pprint as ppr

from lxml import html
import pytz

tz = pytz.timezone("US/Central")
current_date = datetime.today()
current_month = current_date.month
current_year = current_date.year
date_range = []

for x in range(0,4):
    if not current_month == 12:
        cm = current_month
        if len(str(cm)) < 2:
            cm = '0{0}'.format(cm)
        timestamp = "{0}-{1}".format(current_year, cm)
        date_range.append(timestamp)
        current_month += 1

    elif current_month == 12:
        cm = '12'
        timestamp = "{0}-{1}".format(current_year, cm)        
        date_range.append(timestamp)
        current_month = 1
        current_year += 1


class StpaulEventScraper(Scraper):
    global date_range
    def scrape(self):
        #b = requests.get('https://api.mnactivist.org/api/add-event')
        #events = b.json()['results']
        events = []
        uaes = []
        for e in events:
            continue
            if e['city'] == 'Saint Paul':
                uaes.append(e)
            elif e['city'] == 'St Paul':
                e['city'] = 'Saint Paul'
                uaes.append(e)
            elif e['city'] == 'St. Paul':
                e['city'] = 'Saint Paul'
                uaes.append(e)

        for u in uaes:
            continue
            nloc = u['location'].split(' |0| ')
            loc = (' ').join(nloc)
            new_event = Event(name=u['name'],
                      start_date=u['startdate'],
                      location_name=loc,
                      classification=u['event_type'])
            new_event.add_source('https://mnactivist.org')
            yield new_event


        format1 = "%A %B %d, %Y - %I:%M %p"
        format2 = "%A %B %d, %Y - "
        format3 = "%m/%d/%y"
        print(date_range)
        for date in date_range:
            root = requests.get("https://www.stpaul.gov/calendar/" + date)
            base = html.fromstring(root.text)
            items = base.xpath('.//*/div[@class="view-content"]/div')
            meetings = []
            for i in items:
                if len(i.xpath('.//*/span[@class="date-display-single"]/text()')) > 0:
                    d = {}
                    d['date'] = i.xpath('.//*/span[@class="date-display-single"]/text()')[0]
                    d['info'] = i.xpath('.//*/span[@class="field-content"]/a/text()')[0]
                    d['link'] = i.xpath('.//*/span[@class="field-content"]/a/@href')[0]
                    meetings.append(d)
            for m in meetings:
                m['link'] = "https://www.stpaul.gov" + m['link']
            for m in meetings:
                ppr(m['info'])
                r = requests.get(m['link'])
                b = html.fromstring(r.text)
                exists = b.xpath('.//div[@class="node-content clearfix"]')
                if len(exists)>0:
                    date = exists[0].xpath('.//*/span[@class="date-display-single"]/text()')
                    loc1 = exists[0].xpath('.//*/div[@class="thoroughfare"]/text()')
                    loc2 = exists[0].xpath('.//*/div[@class="premise"]/text()')
                    if len(loc1) > 0:
                        print(loc1)
                        m['location'] = loc1[0] 
                    if len(loc2) > 0:
                        print(m)
                        print(loc2)
                        if not len(loc1) > 0:
                            m['location'] = loc2[0]
                        else:
                            m['location'] = m['location'] + " " + loc2[0]
                    else:
                        m['location'] = 'N/A'
                    if ":" in date[0]:
                        m['date'] = datetime.strptime(date[0], format1)
                    elif "/" in date[0]:
                        new_date = date[0].split('/')
                        for n in new_date:
                            if len(n) == 1:
                                n = '0'+ n
                                new_date = '/'.join(new_date)
                                m['date'] = datetime.strptime(new_date, format3)
                    else:
                        date = datetime.strptime(date[0], format2)
                        m['date'] = date
                    m['date'] = tz.localize(m['date'])                        
                    if not 'City Council' in m['info'] and not 'Legislative' in m['info'] and not 'Holiday' in m['info']:

                        event = Event(name=m['info'].strip(),
                                      start_date=m['date'], 
                                      location_name=m['location'],
                                      classification='govt' 
                        )
                        m['name'] = m['info'].replace('Meeting', '').replace(' - Cancelled', '').replace('Events', '').strip()
                        event.add_committee(m['name'])
                    elif 'Holiday' in m['info']:
                        event = Event(name=m['info'].strip(),
                                      start_date=m['date'],
                                      location_name=m['location'],
                                      classification='govt'                                      
                        )
                    else:
                        event = Event(name=m['info'].strip(),
                                      start_date=m['date'],                                       
                                      location_name=m['location'],
                                      classification='govt' 
                        )
                        event.add_committee('Saint Paul City Council')                
                    event.add_source(m['link']) 
                    yield event
            

