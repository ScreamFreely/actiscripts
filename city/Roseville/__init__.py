# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import RosevilleEventScraper
from .people import RosevillePersonScraper
from .bills import RosevilleBillScraper
from .vote_events import RosevilleVoteEventScraper


class Wayzata(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:roseville"
    classification = "government"
    name = "Roseville"
    url = "https://www.cityofroseville.com/"
    scrapers = {
        "events": RosevilleEventScraper,
        # "people": WayzataPersonScraper,
        # "bills": WayzataBillScraper,
        # "vote_events": WayzataVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Roseville', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:roseville')       
        yield city

        council = Organization(name="Roseville City Council", classification="legislature", parent_id=city)
        for x in range(1, 5):
            council.add_post(
                "At-Large {}".format(x),
                "Council member",
                division_id='ocd-division/country:us/state:mn/place:roseville')
        yield council