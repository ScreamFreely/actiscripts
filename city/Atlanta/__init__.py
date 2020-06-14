# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import AtlantaEventScraper
from .people import AtlantaPersonScraper
from .bills import AtlantaBillScraper
from .vote_events import AtlantaVoteEventScraper


class Wayzata(Jurisdiction):
    division_id = "ocd-division/country:us/state:ga/place:atlanta"
    classification = "government"
    name = "Atlanta"
    url = "https://citycouncil.atlantaga.gov/"
    scrapers = {
        "events": AtlantaEventScraper,
        # "people": AtlantaPersonScraper,
        # "bills": AtlantaBillScraper,
        # "vote_events": AtlantaVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('Atlanta', classification='executive')     
        yield city

        # council = Organization(name="Wayzata City Council", classification="legislature", parent_id=city)
        # for x in range(1, 5):
        #     council.add_post(
        #         "At-Large {}".format(x),
        #         "Council member",
        #         division_id='ocd-division/country:us/state:mn/place:wayzata')
        # yield council