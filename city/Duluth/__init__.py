# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import DuluthEventScraper
from .people import DuluthPersonScraper
from .bills import DuluthBillScraper
from .vote_events import DuluthVoteEventScraper


class Duluth(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/county:st_louis/place:duluth"
    classification = "government"
    name = "Duluth"
    url = "http://www.duluthmn.gov"
    scrapers = {
        "events": DuluthEventScraper,
        # "people": DuluthPersonScraper,
        # "bills": DuluthBillScraper,
        # "vote_events": DuluthVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Duluth', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/county:st_louis/place:duluth')
        city.add_post('City Clerk', 'City Clerk', division_id='ocd-division/country:us/state:mn/county:st_louis/place:duluth')        
        yield city

        council = Organization(name="Duluth City Council", classification="legislature", parent_id=city)
        for x in range(1, 6):
            council.add_post(
                "District {}".format(x),
                "Councilmember",
                division_id='ocd-division/country:us/state:mn/county:st_louis/place:duluth/council_district:{}'.format(x)
                )
            if x < 5:
                council.add_post(
                    "At-Large",
                    "Councilmember",
                    )
        yield council
