#!/bin/bash

source /var/www/ACTIBASES/ca.actibase/bin/activate

cd /var/www/ACTIBASES/ca.actibase/actiscripts/city/

pupa update SanFrancisco events
pupa update Oakland events

# cd /var/www/ACTIBASES/ca.actibase/actiscripts/state
# pupa update California events

deactivate

