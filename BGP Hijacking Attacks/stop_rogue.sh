#!/bin/bash

sudo python run.py --node R6 --cmd "pgrep -f [z]ebra-R6 | xargs kill -9"
sudo python run.py --node R6 --cmd "pgrep -f [b]gpd-R6 | xargs kill -9"
