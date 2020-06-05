# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import BrooklynCenterEventScraper
from .people import BrooklynCenterPersonScraper
from .bills import BrooklynCenterBillScraper
from .vote_events import BrooklynCenterVoteEventScraper


class Wayzata(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:brooklyn_center"
    classification = "government"
    name = "Brooklyn Center"
    url = "http://www.cityofbrooklyncenter.org/"
    scrapers = {
        "events": BrooklynCenterEventScraper,
        # "people": WayzataPersonScraper,
        # "bills": WayzataBillScraper,
        # "vote_events": WayzataVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Wayzata', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:brooklyn_center')       
        yield city

        council = Organization(name="Brookly Center City Council", classification="legislature", parent_id=city)
        for x in range(1, 5):
            council.add_post(
                "At-Large {}".format(x),
                "Council member",
                division_id='ocd-division/country:us/state:mn/place:brooklyn_center')
        yield council