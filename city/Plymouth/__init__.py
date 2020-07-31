# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import PlymouthEventScraper
from .people import PlymouthPersonScraper
from .bills import PlymouthBillScraper
from .vote_events import PlymouthVoteEventScraper


class Plymouth(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:plymouth"
    classification = "government"
    name = "Plymouth"
    url = "https://www.plymouthmn.gov/"
    scrapers = {
        "events": PlymouthEventScraper,
        # "people": PlymouthPersonScraper,
        # "bills": PlymouthBillScraper,
        # "vote_events": PlymouthVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Plymouth', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:plymouth')
        city.add_post('City Clerk', 'City Clerk', division_id='ocd-division/country:us/state:mn/place:plymouth')        
        yield city

        council = Organization(name="Minneapolis City Council", classification="legislature", parent_id=city)
        for x in range(1, 5):
            council.add_post(
                "Ward {}".format(x),
                "Councilmember",
                division_id='ocd-division/country:us/state:mn/place:plymouth/ward:{}'.format(x))
            
        yield council
