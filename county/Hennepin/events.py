import requests
import re
import datetime
import pytz
from lxml import html

from pupa.scrape import Scraper
from pupa.scrape import Event


class HennepinEventScraper(Scraper):
    datetime = datetime.datetime
    format = '%B %d, %Y %I:%M %p'
    tz = pytz.timezone("US/Central")

    def run_board_mts(self, board_mtgs):
        tz = pytz.timezone("US/Central")
        format = '%B %d, %Y %I:%M %p'
        events = []
        for b in board_mtgs[1:]:
            info = b.xpath('.//td/text()')
            link_text = b.xpath('.//td/a/text()')
            links = b.xpath('.//td/a/@href')
            nlinks = []
            date = info[0] + ' 1:30 pm'
            real_date = datetime.datetime.strptime(date, format)
            for l in links:
                l = l[22:-2]
                nlinks.append(l)
            clinks = zip(link_text, nlinks)
            enotes = []
            dt = tz.localize(real_date)
            e = Event(
                name='Hennepin County Board',
                start_date=dt,
                location_name='Hennepin County Government Center, 24th floor',
                classification='govt')
            e.add_committee('Hennepin County')
            e.add_source(
                'https://board.co.hennepin.mn.us/hcmeetview/Default.aspx')
            events.append(e)
        return events

    def run_cmt_mts(self, cmt_mtgs):
        tz = pytz.timezone("US/Central")
        format = '%B %d, %Y %I:%M %p'
        for c in cmt_mtgs[1:]:
            info = c.xpath('.//td/text()')
            link_text = c.xpath('.//td/a/text()')
            links = c.xpath('.//td/a/@href')
            nlinks = []
            date = info[0] + ' 1:30 pm'
            real_date = datetime.datetime.strptime(date, format)
            for l in links:
                l = l[22:-2]
                nlinks.append(l)
            clinks = zip(link_text, nlinks)
            enotes = []
            if len(list(clinks)) > 0:
                for i, l in clinks:
                    j = "<a href=\"" + l + "\" target=_blank>" + i + "</a>"
                    print(j)

    def run_auth_mts(self, auth_mtgs):
        tz = pytz.timezone("US/Central")
        format = '%B %d, %Y %I:%M %p'
        for a in auth_mtgs[1:]:
            info = a.xpath('.//td/text()')
            link_text = a.xpath('.//td/a/text()')
            links = a.xpath('.//td/a/@href')
            nlinks = []
            date = info[0] + ' 1:30 pm'
            real_date = datetime.datetime.strptime(date, format)
            for l in links:
                l = l[22:-2]
                nlinks.append(l)
            clinks = zip(link_text, nlinks)
            enotes = []

            if len(list(clinks)) > 0:
                for i, l in clinks:
                    j = "<a href=\"" + l + "\" target=_blank>" + i + "</a>"
                    print(j)

    def scrape(self):
        today = datetime.datetime.today()
        year = today.year

        for x in range(0, 4):
            month = today.month + x
            while month >= 12:
                if x == 0:
                    print('new month ', month)
                    root = requests.get(
                        'https://board.co.hennepin.mn.us/hcmeetview/Default.aspx?year={0}&month={1}'.format(year, month))
                    base = html.fromstring(root.text)
                else:
                    root = requests.get(
                        'https://board.co.hennepin.mn.us/hcmeetview/Default.aspx?year={0}&month={1}'.format(year, x))
                    base = html.fromstring(root.text)
            else:
                print('new month ', month)
                root = requests.get(
                    'https://board.co.hennepin.mn.us/hcmeetview/Default.aspx?year={0}&month={1}'.format(year, month))
                base = html.fromstring(root.text)

            board_mtgs = base.xpath('.//*[@id="tblBoardMeetings"]/tr')
            cmt_mtgs = base.xpath('.//*[@id="tblCommitteeMeetings"]/tr')
            auth_mtgs = base.xpath('.//*[@id="tblAuthorityMeetings"]/tr')

            fmtgs = self.run_board_mts(board_mtgs)
            for f in fmtgs:
                yield f
            self.run_cmt_mts(cmt_mtgs)
            self.run_auth_mts(auth_mtgs)
