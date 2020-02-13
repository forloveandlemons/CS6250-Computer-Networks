#!/bin/bash

node=${1:-h5-1}
bold=`tput bold`
normal=`tput sgr0`

while true; do
    out=`sudo python run.py --node $node --cmd "curl -s 11.0.1.1"`
    date=`date`
    echo $date -- $bold$out$normal
    sleep 1
done

