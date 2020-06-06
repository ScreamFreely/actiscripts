#!/bin/bash

#killall Xvfb

source /var/www/ACTIBASES/ca.actibase/bin/activate

cd /var/www/ACTIBASES/ca.actibase/actibase/scripts/state
pupa update California events bills


deactivate

#killall Xvfb
