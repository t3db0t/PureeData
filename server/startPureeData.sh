#!/bin/bash

#debugging
sudo nohup python pureeDataServer.py 80 &

#production
#sudo nohup python pureeDataServer.py 80 > /dev/null &