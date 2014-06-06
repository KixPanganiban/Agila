#!/bin/bash
# install script for client monitoring scripts
# @author ibaguio

#crontab -l > mycron
#echo "05 09 * * 1-5 echo hello" >> mycron
#crontab mycron
#rm mycron

PATH=$PATH:/usr/local/bin
cp -r scripts /usr/local/bin/climateapp

{
	echo "First use"
	python scripts/firstuse.py
} && {
	echo "installing cron"
	crontab -l | { cat; echo "*/5 * * * * python /usr/local/bin/climateapp/monitor.py"; } | crontab -
}
