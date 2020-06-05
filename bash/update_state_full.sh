#!/bin/bash

#killall Xvfb

source /var/www/mn.actibase/bin/activate

cd /var/www/mn.actibase/actibase/scripts/state
pupa update Minnesota events bills


deactivate

#killall Xvfb
