# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import DenverEventScraper
from .people import DenverPersonScraper
from .bills import DenverBillScraper
from .vote_events import DenverVoteEventScraper


class Denver(Jurisdiction):
    division_id = "ocd-division/country:us/state:co/place:denver"
    classification = "government"
    name = "Denver"
    url = "https://www.denvergov.org/"
    scrapers = {
        "events": DenverEventScraper,
        # "people": DenverPersonScraper,
        # "bills": DenverBillScraper,
        # "vote_events": DenverVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Denver', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:co/place:denver')       
        yield city

        # council = Organization(name="Denver City Council", classification="legislature", parent_id=city)
        # for x in range(1, 5):
        #     council.add_post(
        #         "At-Large {}".format(x),
        #         "Council member",
        #         division_id='ocd-division/country:us/state:mn/place:Denver')
        # yield council