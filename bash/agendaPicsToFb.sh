#!/bin/bash

killall Xvfb

source /var/www/ACTIBASES/il.actibase/bin/activate

python /var/www/ACTIBASES/il.actibase/actibase/scripts/bash/getPics.py

deactivate

killall Xvfb
