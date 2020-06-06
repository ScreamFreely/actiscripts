# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import ChicagoEventScraper
from .people import ChicagoPersonScraper
from .bills import ChicagoBillScraper
from .vote_events import ChicagoVoteEventScraper


class Chicago(Jurisdiction):
    division_id = "ocd-division/country:us/state:il/place:chicago"
    classification = "government"
    name = "Chicago"
    url = "https://www.chicago.gov"
    scrapers = {
        "events": ChicagoEventScraper,
        # "people": ChicagoPersonScraper,
        # "bills": ChicagoBillScraper,
        # "vote_events": ChicagoVoteEventScraper,
    }

    def get_organizations(self):
        #REQUIRED: define an organization using this format
        #where org_name is something like Seattle City Council
        #and classification is described here:
        city = Organization(name="City of Chicago", classification="executive")
        yield city
        
        # OPTIONAL: add posts to your organizaion using this format,
        # where label is a human-readable description of the post (eg "Ward 8 councilmember")
        # and role is the position type (eg councilmember, alderman, mayor...)
        # skip entirely if you're not writing a people scraper.
        # org.add_post(label="position_description", role="position_type")

        #REQUIRED: yield the organization
        # yield org
