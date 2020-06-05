# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import EdinaEventScraper
from .people import EdinaPersonScraper
from .bills import EdinaBillScraper
from .vote_events import EdinaVoteEventScraper


class Wayzata(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:edina"
    classification = "government"
    name = "Edina"
    url = "https://www.edinamn.gov/"
    scrapers = {
        "events": EdinaEventScraper,
        # "people": WayzataPersonScraper,
        # "bills": WayzataBillScraper,
        # "vote_events": WayzataVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Edina', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:edina')       
        yield city

        council = Organization(name="Edina City Council", classification="legislature", parent_id=city)
        for x in range(1, 5):
            council.add_post(
                "At-Large {}".format(x),
                "Council member",
                division_id='ocd-division/country:us/state:mn/place:edina')
        yield council