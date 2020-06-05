# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import BurnsvilleEventScraper
from .people import BurnsvillePersonScraper
from .bills import BurnsvilleBillScraper
from .vote_events import BurnsvilleVoteEventScraper


class Wayzata(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:burnsville"
    classification = "government"
    name = "Burnsville"
    url = "http://www.ci.burnsville.mn.us/"
    scrapers = {
        "events": BurnsvilleEventScraper,
        # "people": WayzataPersonScraper,
        # "bills": WayzataBillScraper,
        # "vote_events": WayzataVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Burnsville', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:burnsville')       
        yield city

        council = Organization(name="Burnsville City Council", classification="legislature", parent_id=city)
        for x in range(1, 17):
            council.add_post(
                "At-Large {}".format(x),
                "Council member",
                division_id='ocd-division/country:us/state:mn/place:burnsville')
        yield council