import sys
import os

import requests, re, datetime
from lxml import html
from xvfbwrapper import Xvfb
from pprint import pprint as ppr
import pytz
from selenium import webdriver as wd


start_cmd = "Xvfb :99 && export DISPLAY=:99 &"
xvfb = Xvfb()

os.system(start_cmd)
xvfb.start()

print("Xvfb started")

br = wd.Chrome()
br.get("https://www.minneapolisparks.org/public_meetings/")
b = html.fromstring(br.page_source)
print("\n\n\nBase obtained\n\n\n")
xvfb.stop()
os.system("pkill Xvfb")

mtgs = b.xpath('.//*/table/*/tr/td[@class="cwuceeventtitle"]')
tz = pytz.timezone("US/Central")

for m in mtgs:
    d = {}
    d['title'] = m.xpath('.//a/text()')[0]
    link = m.xpath('.//a/@onclick')[0]
    link_id = link[link.find("(")+1:link.find(")")]
    nlink = "https://www.calendarwiz.com/calendars/popup.php?op=view&id={0}&crd=mprb".format(link_id)
    r = requests.get(nlink)
    b = html.fromstring(r.text)
    info = m.xpath('.//div/text()')
    dt_info = info[0].split("@")[0].strip()
    print(dt_info)
    if " at " in dt_info:
        format = '%a, %b %d, %Y at %I:%M%p'
        d['time'] = datetime.strptime(dt_info, format)
    elif "from" in dt_info:
        dt_info = dt_info.split("-")[0].strip()
        format = '%a, %b %d, %Y from %I:%M%p'
        d['time'] = datetime.strptime(dt_info, format)
    elif " to " in dt_info:
        continue
    elif "-" in dt_info:
        ndt = dt_info.split("-")[0].strip()
        format = '%a, %b %d, %Y %I:%M%p'
        d['time'] = datetime.strptime(ndt, format)
    else:
        format = '%a, %b %d, %Y %I:%M%p'
        d['time'] = datetime.strptime(dt_info, format)

    loc, details = [], []
    for l in b.xpath('.//*[@id="event_details"]/text()'):
        l = l.replace("\n", "").replace("\t", "").strip()
        if len(l)>0:
            loc.append(l)
    for l in b.xpath('.//*[@id="event_details"]/div/text()'):
        l = l.replace("\n", "").replace("\t", "").strip()
        if len(l)>0:
            details.append(l)
    for l in b.xpath('.//*[@id="event_details"]/div/p/a'):
        link = l.xpath('.//@href')
        link_title = l.xpath('.//text()')
        link_str = '<a href="{0}" target="_blank">{1}</a>'.format(link[0], link_title[0])
        rd = requests.get(link[0])
        bd = html.fromstring(rd.text)
        rows = bd.xpath('.//*/div[@class="Row MeetingRow"]')
        for rw in rows:
            link = rw.xpath('.//*/div[@class="RowLink"]/a/@href')
            etime = rw.xpath('.//*/div[@class="RowLink"]/a/text()')
            format = '%b %d, %Y %I:%M %p'
            etime = datetime.strptime(etime[0].strip(), format)
            if d['time'].date() == etime.date():
                if d['time'].hour == etime.hour:
                    deets = rw.xpath('.//*/div[@class="RowRight MeetingLinks"]/a/text()')
                    dlinks = rw.xpath('.//*/div[@class="RowRight MeetingLinks"]/a/@href')
                    print("\n\n\n\n\n{0}\n\n\n\n\n".format(deets))
        details.append(link_str)
    d['location'] = "<br/>".join(loc)
    d['link'] = nlink
    d['loc_info'] = info[0].split("@")[1]
    if len(details)>0:
        d['details'] = details[0]
        d['zfo'] = d['details'] + "<br/><br/> " + d['loc_info'] + "<br/>" + d['location']
    else:
        d['zfo'] = d['loc_info'] + "<br/> " + d['location']

    dt = tz.localize(d['time'])
    location = d['loc_info'] + ' ' + d['location']
    if d['title'] == 'Board Meeting':
        event_title = 'Mpls Park & Rec Board Meeting'
    else:
        event_title = d['title']
    e = Event(name=event_title,start_date=dt,location_name=location, classification='govt')
    if d['title'] == 'Board Meeting':
        e.add_committee(d['CommitteeName'])
    e.add_source(d['link'])
    yield e
