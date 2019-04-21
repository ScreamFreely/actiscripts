from pupa.scrape import Scraper
from pupa.scrape import Event

from lxml import html
from datetime import datetime, timedelta
import requests

import pytz

tz = pytz.timezone("US/Central")

DATE_FORMAT = '%B %d, %Y %I%p'


site = requests.get(
    'http://www.ci.inver-grove-heights.mn.us/272/Meetings-Schedule')
base = html.fromstring(site.text)
months = base.xpath('.//*/table/tbody/tr/td')

isDigit = 0
holdNumber = ''

FINAL_DATES = []

for m in months:
    month = m.xpath('.//h3/text()')[0]
    # bolded = m.xpath('.//strong/text()')
    allText = m.xpath('.//text()')[1:]
    nAllText = []
    for a in allText:
        a = a.replace('\n', '').replace(':', '').strip()
        if len(a) > 0:
            if a.isdigit() == True:
                if isDigit == 0:
                    holdNumber = a
                    isDigit = 1
                else:
                    holdNumber = holdNumber + a
            elif a == 'TBD':
                holdNumber = 'TBD'
                isDigit = 0
            elif a == '(Tuesday)':
                isDigit = 0
            else:
                nText = holdNumber +  ' ' + a
                d = {}
                d['info'] = a
                d['location'] = 'Inver Grove Heights City Hall, 8150 Barbara Avenue, MN 55077'
                if d['info'] == 'Regular meeting':
                    d['date'] = "{0} {1}, {2} {3}".format(month, holdNumber, '2018', '7pm')
                    FINAL_DATES.append(d)
                    isDigit = 0
                elif d['info'] == 'Work Session':
                    d['date'] = "{0} {1}, {2} {3}".format(month, holdNumber, '2018', '6pm')
                    FINAL_DATES.append(d)
                    isDigit = 0
                else:
                    isDigit = 0              

class InvergroveheightsEventScraper(Scraper):

    def scrape(self):
        for c in FINAL_DATES:
            mtg_time = datetime.strptime(c['date'], DATE_FORMAT)
            dt = tz.localize(mtg_time)
            e = Event(name=c['info'],
                      start_date=dt,
                      location_name=c['location'],
                      classification='govt')
            # e.add_committee(c['CommitteeName'])
            e.add_source('http://www.ci.inver-grove-heights.mn.us/272/Meetings-Schedule')
            # e.add_media_link(note="Map link",
            #                  url=c['locationLink'],
            #                  media_type="link")
            # if c['MarkedAgendaPublished'] == True:
            #     event_url = "{0}{1}/{2}".format(AGENDA_BASE_URL, c['Abbreviation'], c['AgendaId'])
            #     e.add_media_link(note="Agenda",
            #                      url=event_url,
            #                      media_type="link")
            yield e
