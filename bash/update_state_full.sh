#!/bin/bash

#killall Xvfb

source /var/www/mn.actibase/bin/activate

cd /var/www/mn.actibase/actibase/scripts/state
pupa update Minnesota house senate comms bills


deactivate

#killall Xvfb
