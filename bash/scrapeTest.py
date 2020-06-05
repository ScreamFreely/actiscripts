import sys
import os
import django
from pprint import pprint as ppr


sys.path.append('/var/www/mn.actibase/actibase/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Actibase.settings'
django.setup()

from dex.models import UserAddedEvent as UAE
from dex.models import FBEvent as FBE

import requests
from lxml import html
from pprint import pprint as ppr


import re, os
from datetime import datetime

from time import sleep
from pprint import pprint as ppr
from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException

from xvfbwrapper import Xvfb


os.system('pkill Xvfb')

start_cmd = "Xvfb :71 && export DISPLAY=:71 &"
xvfb = Xvfb()

os.system(start_cmd)

def get_base(site):
	xvfb.start()
	br = wd.Chrome()
	br.get(site)
	sleep(8)
	base = html.fromstring(br.page_source)
	xvfb.stop()
	return base

fb_events = FBE.objects.all()
format1 = '%A, %B %d %I:%M %p %Y'

for fb in fb_events:
    if 'event_time_id' in fb.link:
        continue 
    if fb.published == True:
        continue 
    base = get_base(fb.link)
    date = base.xpath('.//*/span[@itemprop="startDate"]/text()')[0]
    times = base.xpath('.//*/li/div/table/tbody/tr/td/div/div/div/div/div/span/text()')
    loc = base.xpath('.//*/li/div/table/tbody/tr/td/div/div/div/div/div/span/span/text()')
    if len(loc)< 2: 
        ppr(loc)
        loc = 'n/a'
    else:
        loc = loc[1]
    title = base.xpath('.//*/h1/text()')[0]
    deets = base.xpath('.//*/div[@id="reaction_units"]/div/div/div/div/div/div/div/span/text()')
    
    deets = ('\n\n').join(deets)
    print(title)
    print(fb.link)
    ppr(times)
    startTime = times[0]
    if 'CDT' in startTime:
        startTime = startTime.replace('CDT', '').strip()
    startTime = startTime + ' 2018'
    if len(times)>1:
        endTime = times[1]
    if len(times) == 3:
        zip_code = times[2]
    else:
        zip_code = '000000'
    date = date + ' ' + startTime
    if not loc == 'n/a':
        city = loc.split(',')[1]
    else:
        city = 'na'
    loc = loc + zip_code
    real_date = datetime.strptime(date, format1)
    
    event, c = UAE.objects.get_or_create(name=title,city=city, location=loc, startdate=real_date, description=deets, link=fb.link, published='f')

    ppr(event)
    fb.published = 't'
    fb.save()
