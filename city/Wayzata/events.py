from pupa.scrape import Scraper
from pupa.scrape import Event

from datetime import datetime, timedelta
import requests
from lxml import html

import pytz

tz = pytz.timezone("US/Central")

DATE_FORMAT = '%B %d, %Y %I:%M %p'

site = requests.get('https://www.wayzata.org/RSSFeed.aspx?ModID=58&CID=All-calendar.xml')
base = html.fromstring(site.text)
events = base.xpath('.//*/item')

EVENTS = []

for e in events:
    d = {}
    d['title'] = e.xpath('.//title/text()')[0]
    d['link'] = e.xpath('.//guid/text()')[0]
    eventDates = e.xpath('.//eventdates/text()')[0].strip()
    eventTimes = e.xpath('.//eventtimes/text()')[0].split('-')[0].strip()
    dateTime = eventDates + ' ' + eventTimes
    d['dateTime'] = datetime.strptime(dateTime, DATE_FORMAT)
    d['location'] = e.xpath('.//location/text()')[0].replace('<br>', ' ')
    
    desc = e.xpath('.//description/text()')[0]
    newBase = html.fromstring(desc)
    bolded = newBase.xpath('.//strong/text()')
    if 'Description:' in bolded:
        nText = newBase.xpath('.//text()')
        print(nText)
        try:
            d['description'] = nText[9]
        except:
            d['description'] = nText[8]
    EVENTS.append(d)


class WayzataEventScraper(Scraper):

    def scrape(self):
        for c in EVENTS:
            dt = tz.localize(c['dateTime'])
            e = Event(name=c['title'],
                      start_date=dt,
                      location_name=c['location'],
                      classification='govt')
            # e.add_committee(c['CommitteeName'])
            e.add_source('https://www.wayzata.org/RSSFeed.aspx?ModID=58&CID=All-calendar.xml')
            e.add_media_link(note="Event link",
                             url=c['link'],
                             media_type="link")
            # if c['MarkedAgendaPublished'] == True:
            #     event_url = "{0}{1}/{2}".format(AGENDA_BASE_URL, c['Abbreviation'], c['AgendaId'])
            #     e.add_media_link(note="Agenda",
            #                      url=event_url,
            #                      media_type="link")
            yield e
