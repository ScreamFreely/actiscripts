#!/bin/bash

killall Xvfb

source /var/www//mn.actibase/bin/activate

python /var/www/mn.actibase/actibase/scripts/bash/getPics.py

deactivate

killall Xvfb
