# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import InvergroveheightsEventScraper
from .people import InvergroveheightsPersonScraper
from .bills import InvergroveheightsBillScraper
from .vote_events import InvergroveheightsVoteEventScraper


class Invergroveheights(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:inver_grove_heights"
    classification = "government"
    name = "Inver Grove Heights"
    url = "http://www.ci.inver-grove-heights.mn.us"
    scrapers = {
        "events": InvergroveheightsEventScraper,
        # "people": InvergroveheightsPersonScraper,
        # "bills": InvergroveheightsBillScraper,
        # "vote_events": InvergroveheightsVoteEventScraper,
    }

    def get_organizations(self):
        city = Organization('City of Inver Grove Heights', classification='executive')
        city.add_post('Mayor', 'Mayor', division_id='ocd-division/country:us/state:mn/place:inver_grove_heights')       
        yield city

        council = Organization(name="Inver Grove Heights City Council", classification="legislature", parent_id=city)
        for x in range(1, 5):
            council.add_post(
                "At-Large {}".format(x),
                "Council member",
                division_id='ocd-division/country:us/state:mn/place:inver_grove_heights')
        yield council
