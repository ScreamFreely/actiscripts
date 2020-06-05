#!/bin/bash

#killall Xvfb

source /var/www/mn.actibase/bin/activate

cd /var/www/mn.actibase/actiscripts/state
pupa update Minnesota bills 

deactivate

#killall Xvfb
