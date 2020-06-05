# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import StCloudEventScraper
from .people import StCloudPersonScraper
from .bills import StCloudBillScraper
from .vote_events import StCloudVoteEventScraper


class Wayzata(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:st_cloud"
    classification = "government"
    name = "Saint Cloud"
    url = "https://www.wayzata.org/"
    scrapers = {
        "events": StCloudEventScraper,
        # "people": WayzataPersonScraper,
        # "bills": WayzataBillScraper,
        # "vote_events": WayzataVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of St Cloud', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:st_cloud')       
        yield city

        council = Organization(name="St Cloud City Council", classification="legislature", parent_id=city)
        for x in range(1, 5):
            council.add_post(
                "At-Large {}".format(x),
                "Council member",
                division_id='ocd-division/country:us/state:mn/place:st_cloud')
        yield council