#!/usr/bin/env python
# firstuse.py
# script to run to initialized the script
# @author ibaguio
import constants, urllib, json, logging
import re, uuid

def run():
	import multiprocessing, platform

	while True:
		token = raw_input("Please enter unique token: ")

		data = {'cores': multiprocessing.cpu_count(),
				'os': platform.uname()[0],
				'mac': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
				'token': token}

		try:
			url = "http://"+ constants.SERVER +"/cgi/init/"
			encoded = urllib.urlencode(data)
			data = urllib.urlopen(url,encoded)
			reponse = json.loads(data.read())
			if reponse['status'] != 'invalid_token':
				break
			elif reponse['status'] != 'invalid':
				print "Error occured"
				break
			else:
				print "Invalid token."
		except IOError:
			print "Internet connection needed"
			break
		except Exception, e:
			logging.exception('error')
			break

	#device mac address
	#os details
	#device cores
	#hardware
	#models

if __name__ == '__main__':
	run()