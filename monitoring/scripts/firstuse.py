#!/usr/bin/env python
# firstuse.py
# script to run to initialized the script
# @author ibaguio
import constants, urllib, json, logging
def run():
	import multiprocessing, platform

	data = {'cores': multiprocessing.cpu_count(),
			'os': platform.uname()[0],

	try:
		url = "http://"+ constants.SERVER +"/cgi/init/"
		encoded = urllib.urlencode(data)
		urllib.urlopen(url,encoded)
		reponse = json.dumps(urllib.read())

		print reponse
	except IOError:
		print "Internet connection needed"
	except Exception, e:
		logging.exception('error')
	
	#device mac address
	#os details
	#device cores
	#hardware
	#models

if __name__ == '__main__':
	run()