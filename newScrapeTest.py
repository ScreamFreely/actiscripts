import requests

from pprint import pprint as ppr

from lxml import html


site = requests.get('https://www.stlouispark.org/government/city-council/meetings')

base = html.fromstring(site.text)

print(base)

rows = base.xpath('.//*/table/tbody/tr')

for r in rows:
	d = {}
	cells = r.xpath('.//td/text()')
	d['title'] = 
	d['datetime'] =
	d['location'] = 
	ppr(d)

# ppr(rows)



