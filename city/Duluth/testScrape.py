from pprint import pprint as ppr

import requests
from lxml import html

city_url = 'http://www.duluthmn.gov'
council_url = 'http://www.duluthmn.gov/city-council/city-councilors'

def get_base(site):
	s = requests.get(site)
	b = html.fromstring(s.text)
	return b


council = get_base(council_url)
members = council.xpath('.//*/div[@id="divPageContent"]/*[@id="divRight"]/ul/li')
for m in members:
	name = m.xpath('.//a/text()')[0]
	link = m.xpath('.//a/@href')[0]
	mlink = city_url+link
	print(name, mlink)
	member = get_base(mlink)
	info = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/span/text()')
	text = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/span/span/text()')
	email = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/span/a/text()')
	links = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/span/span/span/a')
	mlinks = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/a/text()')
	# ppr(info)
	if len(email)>0:
		ppr(email[0])
	else:
		ppr(mlinks[0])
	# ppr(text)
	# ppr(links)
	# ppr(mlinks)
	print('+++ \n\n +++')