# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import OaklandEventScraper
from .people import OaklandPersonScraper
from .bills import OaklandBillScraper
from .vote_events import OaklandVoteEventScraper


class Oakland(Jurisdiction):
    division_id = "ocd-division/country:us/state:ca/place:oakland"
    classification = "government"
    name = "Oakland"
    url = "https://www.oaklandca.gov/"
    scrapers = {
        "events": OaklandEventScraper,
        # "people": OaklandPersonScraper,
        # "bills": OaklandBillScraper,
        # "vote_events": OaklandVoteEventScraper,
    }

    def get_organizations(self):
        #REQUIRED: define an organization using this format
        #where org_name is something like Seattle City Council
        #and classification is described here:
        city = Organization('City of Oakland', classification='executive')
        yield city

        # OPTIONAL: add posts to your organizaion using this format,
        # where label is a human-readable description of the post (eg "Ward 8 councilmember")
        # and role is the position type (eg councilmember, alderman, mayor...)
        # skip entirely if you're not writing a people scraper.
        # org.add_post(label="position_description", role="position_type")

        #REQUIRED: yield the organization
        # yield org
