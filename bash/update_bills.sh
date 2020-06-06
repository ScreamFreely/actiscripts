#!/bin/bash

#killall Xvfb

source /var/www/ACTIBASES/ca.actibase/bin/activate

cd /var/www/ACTIBASES/ca.actibase/actiscripts/state
pupa update California bills 

deactivate

#killall Xvfb
