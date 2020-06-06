#!/bin/bash

#killall Xvfb

source /var/www/ACTIBASES/il.actibase/bin/activate

cd /var/www/ACTIBASES/il.actibase/actibase/scripts/state
pupa update Illinois


deactivate

#killall Xvfb
