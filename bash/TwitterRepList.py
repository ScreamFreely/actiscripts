import sys
import csv

from pprint import pprint as ppr

import twitter


sys.path.insert(0, '/var/www/mn.actibase')
#sys.path.insert(0, '/home/nkfx/ScreamFreely/MnActivist/server')
import siteauth as KF

data = []

with open('replist.csv', 'r') as f:
	rows = csv.DictReader(f, delimiter=',')
	for row in rows:
		data.append(row)

mnact = {'access_token': KF.fb_token, 'id': KF.fb_id}

api = twitter.Api(consumer_key=KF.tw_ckey,
                  consumer_secret=KF.tw_csecret,
                  access_token_key=KF.tw_tkey,
                  access_token_secret=KF.tw_tsecret)

#CreateListsMember(list_id=None, slug=None, user_id=None, screen_name=None, owner_screen_name=None, owner_id=None)

lists = api.GetListsList()

for l in lists:
	print(l.slug, l.id)

ppr(data[30])

for d in data:
	if d['Currently in Office'] != 'Current':
		print(d['Twitter'], d['Party'], d['Title'])

# for d in data:
# 	if len(d['Twitter']) > 0 and d['Twitter'] != 'none':
# 		twitname = d['Twitter'].replace('@', '')
# 		print(twitname)
# 		try:
# 			if 'House' in d['Title']:
# 				if d['Party'] == 'D':
# 					api.CreateListsMember(list_id='1267556271512866821', screen_name=twitname,)
# 				if d['Party'] == 'R':
# 					api.CreateListsMember(list_id='1267556355252064256', screen_name=twitname,)
# 			if 'Senate' in d['Title']:
# 				if d['Party'] == 'D':
# 					api.CreateListsMember(list_id='1267687801342038016', screen_name=twitname,)
# 				if d['Party'] == 'R':
# 					api.CreateListsMember(list_id='1267970746502066177', screen_name=twitname,)
# 		except Exception as e:
# 			continue
