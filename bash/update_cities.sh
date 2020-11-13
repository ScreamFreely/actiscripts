#!/bin/bash

source /var/www/ACTIBASES/il.actibase/bin/activate

cd /var/www/ACTIBASES/il.actibase/actiscripts/city/

pupa update Chicago events

pkill Xvfb

deactivate

