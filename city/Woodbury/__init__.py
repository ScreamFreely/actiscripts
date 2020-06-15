# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import WoodburyEventScraper
from .people import WoodburyPersonScraper
from .bills import WoodburyBillScraper
from .vote_events import WoodburyVoteEventScraper


class Woodbury(Jurisdiction):
    division_id = "ocd-division/country:us/state:mn/place:woodbury"
    classification = "government"
    name = "Woodbury"
    url = "https://www.woodburymn.gov/"
    scrapers = {
        "events": WoodburyEventScraper,
        "people": WoodburyPersonScraper,
        "bills": WoodburyBillScraper,
        "vote_events": WoodburyVoteEventScraper,
    }

    def get_organizations(self):
        #REQUIRED: define an organization using this format
        #where org_name is something like Seattle City Council
        #and classification is described here:
        city = Organization(name="Woodbury", classification="legislature")
        yield city
        
        # OPTIONAL: add posts to your organizaion using this format,
        # where label is a human-readable description of the post (eg "Ward 8 councilmember")
        # and role is the position type (eg councilmember, alderman, mayor...)
        # skip entirely if you're not writing a people scraper.
        # org.add_post(label="position_description", role="position_type")

        #REQUIRED: yield the organization
        # yield org
