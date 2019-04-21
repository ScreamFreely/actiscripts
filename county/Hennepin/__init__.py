# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import HennepinEventScraper
from .people import HennepinPersonScraper
from .bills import HennepinBillScraper
from .vote_events import HennepinVoteEventScraper


class Hennepin(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/county:hennepin"
    classification = "government"
    name = "Hennepin County"
    url = "https://www.hennepin.us"
    scrapers = {
        "events": HennepinEventScraper,
        "people": HennepinPersonScraper,
        # "bills": HennepinBillScraper,
        # "vote_events": HennepinVoteEventScraper,
    }

    def get_organizations(self):

        hpn = Organization(name="Hennepin County", classification="legislature")
        hpn.add_post("County Attorney", "County Attorney")
        hpn.add_post("Sheriff", "Sheriff")

        for x in range(1, 8):
            hpn.add_post(
                "District {}".format(x),
                "Commissioner",
                division_id='ocd-division/country:us/state:mn/county:hennepin/council_district:{}'.format(x))
        yield hpn
        # org = Organization(name="Housing and Redevelopment Authority", classification="committee")
        # yield org
        # org = Organization(name="Regional Railroad Authority", classification="committee")        
        # yield org
        
