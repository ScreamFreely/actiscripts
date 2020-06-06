import sys
import os
import django
from pprint import pprint as ppr


sys.path.append('/var/www/ACTIBASES/ca.actibase/actibase/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
django.setup()

from lxml import html
import requests, re
from datetime import datetime

from dex.models import UserAddedEvent as UAE 

from opencivicdata.legislative.models import Event

