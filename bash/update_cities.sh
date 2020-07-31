#!/bin/bash

source /var/www/mn.actibase/bin/activate

cd /var/www/mn.actibase/actiscripts/county/

pupa update Hennepin events
pkill Xvfb

cd /var/www/mn.actibase/actiscripts/city/

pupa update Minneapolis events
pupa update StPaul events
pupa update Duluth events
pupa update Woodbury events

cd /var/www/mn.actibase/actiscripts/state
pupa update Minnesota events

deactivate

