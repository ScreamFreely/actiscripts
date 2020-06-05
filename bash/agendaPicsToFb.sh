#!/bin/bash

killall Xvfb

source /var/www//mn.actibase/bin/activate

python /var/www/mn.actibase/actiscripts/bash/getPics.py
cd /var/www/mn.actibase/actiscripts/bash
rm -rf *png

deactivate

killall Xvfb
