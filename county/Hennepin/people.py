import requests
import re
import datetime
from lxml import html

from pupa.scrape import Scraper
from pupa.scrape import Person


class HennepinPersonScraper(Scraper):

    def scrape(self):
        broot = requests.get('https://www.hennepin.us/your-government#leadership')
        base = html.fromstring(broot.text)
        grids = base.xpath('.//*[@class="module-grid"]/article')
        for g in grids:
            c = {}
            c['link'] = g.xpath('.//*/@href')[0]
            if not c['link'].startswith('http'):
                c['link'] = 'https://www.hennepin.us' + c['link']
            name = g.xpath('.//h1/text()')[0]
            print('printedlink:', c['link'])
            if 'hennepinattorney.org' in c['link']:
                print('pass this attn')
                continue

            if 'hennepinsheriff.org' in c['link']:
                print('pass this shrf')
                continue

            clink = c['link']
            cr = requests.get(c['link'])
            cb = html.fromstring(cr.text)
            cbase = cb.xpath('.//*[@class="street-address"]')[0]
            blocks = cbase.xpath('.//*[@class="contactBlock"]')
            for bl in blocks:
                bname = bl.xpath('.//h3/text()')[0]
                email = bl.xpath('.//*/@href')[0].replace('mailto:', '')
                phone = bl.xpath('.//p/text()')[0].replace('Phone: ', '')
                text = bl.xpath('.//p/text()')
                if ',' in bname:
                    bname = bname.split(',')
                    aname = bname[0]
                    position = bname[1]
                    print('{0}: {1}'.format(position, aname))
                    print('{0}: {1}'.format(email, phone))
                else:
                    bname = bname.replace('Commissioner', '').strip()
                    district = 'District ' + clink.split('/')[-1:][0][0]
                    member = Person(name=bname, role='Commissioner')
                    member.add_source(clink)
                    member.add_term('Commissioner','legislature',org_name='Hennepin County',district=district)
                    yield member
                    print('{0}: {1}'.format(email, phone))
                    nclink = clink.split('/')[-1:][0][0]
                    print(nclink)
