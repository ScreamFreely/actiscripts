#!/bin/bash

bash /var/www/mn.actibase/actiscripts/bash/update_cities.sh

killall Xvfb

source /var/www//mn.actibase/bin/activate

python /var/www/mn.actibase/actiscripts/bash/getPics.py

cd /var/www/mn.actibase/actiscripts/bash

rm -rf *png

deactivate

killall Xvfb
