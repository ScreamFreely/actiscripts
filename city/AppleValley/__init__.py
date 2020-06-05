# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import AppleValleyEventScraper
from .people import AppleValleyPersonScraper
from .bills import AppleValleyBillScraper
from .vote_events import AppleValleyVoteEventScraper


class Wayzata(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:apple_valley"
    classification = "government"
    name = "Wayzata"
    url = "https://www.ci.apple-valley.mn.us/"
    scrapers = {
        "events": AppleValleyEventScraper,
        # "people": WayzataPersonScraper,
        # "bills": WayzataBillScraper,
        # "vote_events": WayzataVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Apple Valley', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:apple_valley')       
        yield city

        council = Organization(name="Apple Valley City Council", classification="legislature", parent_id=city)
        for x in range(1, 5):
            council.add_post(
                "At-Large {}".format(x),
                "Council member",
                division_id='ocd-division/country:us/state:mn/place:apple_valley')
        yield council