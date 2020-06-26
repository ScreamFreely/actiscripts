import sys
import os
import re
import random
import time

from io import BytesIO 
from PIL import Image

import requests
from datetime import datetime
from pprint import pprint as ppr

from lxml import html
from selenium import webdriver as wd
import facebook, twitter

from xvfbwrapper import Xvfb

sys.path.insert(0, '/var/www/mn.actibase')
#sys.path.insert(0, '/home/nkfx/ScreamFreely/MnActivist/server')
import siteauth as KF

LINKS = [
    {'cal': 'https://mnactivist.org/p/Minnesota', 'vidlink': None, 'callink': 'http://www.leg.state.mn.us/calendarday.aspx?jday=all'},
    {'cal': 'https://mnactivist.org/p/Minneapolis', 'vidlink': 'http://minneapolismn.gov/tv/citycounciltv', 'callink': 'https://lims.minneapolismn.gov/Calendar/citycouncil/upcoming'},
    {'cal': 'https://mnactivist.org/p/Saint-Paul', 'vidlink': None, 'callink': 'https://www.wayzata.org/RSSFeed.aspx?ModID=58&CID=All-calendar.xml'},
    {'cal': 'https://mnactivist.org/p/Duluth', 'vidlink': None, 'callink': 'https://duluthmn.gov/event-calendar/'},
]

PROMO_LINKS = [
    {'text': "If you'd like to support the work ...", 'link': 'https://teespring.com/otro-sf-cu'},
    {'text': "Got another shirt/sweater/onsie style with the MnActivist logo too :)", 'link': 'https://teespring.com/otro-mnactivist-big-logo-cu'},
    {'text': "Here's a song written and sung by me - a song for you.", 'link': 'https://soundcloud.com/cultureclap/one-sun-one-love'},
    {'text': "And if you'd like to a lil' background on who the captain of this ol' ship is ...", 'link': 'https://blog.cultureclap.com/2020/06/14/activist-project-about/'},
    {'text': "Lastly, you can find all of the code here", 'link': 'https://www.github.com/screamfreely'},
    {'text': "Actually, one last thing, if you'd like to learn how to code, there's some intro material here:", 'link': 'https://www.rebelcoding.com'},
]



mnact = {'access_token': KF.fb_token, 'id': KF.fb_id}

#os.system('killall Xvfb')

start_cmd = "Xvfb :90 && export DISPLAY=:90 &"
xvfb = Xvfb()

os.system(start_cmd)
xvfb.start()
print("Xvfb started")

br = wd.Chrome()
# br = wd.Firefox()
br.set_window_size(800, 1000)

# graph = facebook.GraphAPI(mnact['access_token'], 2.7)
api = twitter.Api(consumer_key=KF.tw_ckey,
                  consumer_secret=KF.tw_csecret,
                  access_token_key=KF.tw_tkey,
                  access_token_secret=KF.tw_tsecret)

lastTweetID = 0

for link in LINKS:
    wait = random.randrange(14, 38, 4)
    br.get(link['cal'])
    timestamp = '{:%Y%m%d-%H:%M:%S}'.format(datetime.now())
    name = link['cal'].split('/')[-1:]
    name = ('-').join(name)
    picName = name + timestamp + '.png'
    time.sleep(10)
    br.get_screenshot_as_file('testShot.png') 
    screen = br.get_screenshot_as_png()
    box = (50, 100, 700, 850)
    im = Image.open(BytesIO(screen))
    region = im.crop(box)
    region.save(picName, 'PNG', optimize=True, quality=95)
    print('Picture save: {0}'.format(picName))
    image=open(picName, 'rb')
    name = name.replace('-', ' ')
    msg = "Upcoming events for {0}\n".format(name)
    if link['vidlink'] != None:
        msg = msg + "\nWatch Online: {0}\n".format(link['vidlink'])
    if link['callink'] != None:
        msg = msg + "\nOfficial Calendar: {0}\n".format(link['callink'])
    if lastTweetID > 0:
        tweet = api.PostUpdate(msg, in_reply_to_status_id=int(lastTweetID), media=image)
    else:
        msg = "THREAD of Upcoming Events:\n\n" + msg
        tweet = api.PostUpdate(msg, media=image)
    lastTweetID = tweet.id
    time.sleep(wait)

for pl in PROMO_LINKS:
    msg = "{0} \n\n {1}".format(pl['text'], pl['link'])
    tweet = api.PostUpdate(msg, in_reply_to_status_id=int(lastTweetID))
    lastTweetID = tweet.id
    time.sleep(wait)




# for link in LINKS:
#     wait = random.randrange(174, 348, 16)
#     br.get(link)
#     timestamp = '{:%Y%m%d-%H:%M:%S}'.format(datetime.now())
#     name = link.split('/')[-1:]
#     name = ('-').join(name)
#     picName = name + timestamp + '.png'
#     time.sleep(5)
#     br.get_screenshot_as_file('testShot.png') 
#     screen = br.get_screenshot_as_png()
#     box = (50, 100, 700, 850)
#     im = Image.open(BytesIO(screen))
#     region = im.crop(box)
#     region.save(picName, 'PNG', optimize=True, quality=95)
#     print('Picture save: {0}'.format(picName))
#     msg = "More at MnActivist.org"
#     image=open(picName, 'rb')
#     graph.put_photo(image=image, album_path= mnact['id'] + "/photos", caption=msg)
#     name = name.replace('-', ' ')
#     api.PostUpdate('Upcoming events for {0}'.format(name), media=image)
#     time.sleep(wait)

# api.PostUpdate('Check us out for Android {0} \n\n and iTunes {1}'.format('http://bit.ly/MnActivist_for_Android', 'http://bit.ly/MnActivist_for_iOS'),)
    
br.close() 
xvfb.stop()
#os.system("pkill Xvfb")
os.system("rm *.png")


