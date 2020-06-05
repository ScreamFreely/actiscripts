#!/bin/bash

killall Xvfb

source /var/www//mn.actibase/bin/activate

python /var/www/mn.actibase/actibase/scripts/bash/getPics.py
cd /var/www/mn.actibase/actibase/scripts/bash
rm -rf *png

deactivate

killall Xvfb
