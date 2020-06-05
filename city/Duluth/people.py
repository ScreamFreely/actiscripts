from pupa.scrape import Scraper
from pupa.scrape import Person


class DuluthPersonScraper(Scraper):

    def scrape(self):
        # City Council

        council = 'http://www.duluthmn.gov/city-council/city-councilors/'
        body = requests.get(council)
        base = html.fromstring(body.text)
        base.make_links_absolute(council)
        wards = base.xpath('.//*/ul[@id="cname"]/li')
        for w in wards:
            i = {}
            link =  w.xpath('.//a/@href')[0]
            text =  w.xpath('.//a/text()')[0]
            i['link'] = link
            i['ward'] = text.split('-')[0].strip()
            i['name'] = text.split('-')[1].strip()
            member = Person(name=i['name'], role='Council Member')
            member.add_source(link)
            member.add_term('Councilmember', 'legislature', org_name='Duluth City Council', district=i['ward'])
            yield member
