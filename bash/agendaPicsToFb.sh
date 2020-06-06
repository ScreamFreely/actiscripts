#!/bin/bash

bash /var/www/ACTIBASES/ca.actibase/actiscripts/bash/update_cities.sh

killall Xvfb

source /var/www//ACTIBASES/ca.actibase/bin/activate

python /var/www/ACTIBASES/ca.actibase/actiscripts/bash/getPics.py

cd /var/www/ACTIBASES/ca.actibase/actiscripts/bash

rm -rf *png

deactivate

killall Xvfb
