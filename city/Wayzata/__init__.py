# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import WayzataEventScraper
from .people import WayzataPersonScraper
from .bills import WayzataBillScraper
from .vote_events import WayzataVoteEventScraper


class Wayzata(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:wayzata"
    classification = "government"
    name = "Wayzata"
    url = "https://www.wayzata.org/"
    scrapers = {
        "events": WayzataEventScraper,
        # "people": WayzataPersonScraper,
        # "bills": WayzataBillScraper,
        # "vote_events": WayzataVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Wayzata', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:wayzata')       
        yield city

        council = Organization(name="Wayzata City Council", classification="legislature", parent_id=city)
        for x in range(1, 5):
            council.add_post(
                "At-Large {}".format(x),
                "Council member",
                division_id='ocd-division/country:us/state:mn/place:wayzata')
        yield council