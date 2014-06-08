#!/usr/bin/env python
# firstuse.py
# script to run to initialized the script
# @author ibaguio
import constants, urllib, json, logging
import re, uuid
from models import TokenManager

def print_ascii():
    print """ AGILA - Carbon Footprint Tracker
               _
       .---.  / > .---,
        <_  `'  `'  _>
          <_/\  /\_>
             /`'\\
            ".__." """

def run():
    import multiprocessing, platform
    print_ascii()
    print "Trying to connect with the server..."

    token = TokenManager.get_or_generate()

    data = {'cores': multiprocessing.cpu_count(),
            'os': platform.uname()[0],
            'mac': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'token': token}

    try:
        url = "http://"+ constants.SERVER +"/cgi/init/"
        encoded = urllib.urlencode(data)
        data = urllib.urlopen(url,encoded)
        reponse = json.loads(data.read())

        if reponse['status'] == 'fail':
            print "Server responded with an error!"
        elif reponse['status'] == 'already_exist':
            print "This Client is already registered"
        elif reponse['status'] == 'error':
            print "An Error occured"
        elif reponse['status'] == 'invalid':
            print "Invalid request"
        elif reponse['status'] == 'ok':
            print "======================================"
            print "        Unique token generated"
            print "          Your token is: %s"%(token)
            print "  use this to uniquely identify this"
            print "  machine over the cloud dashboard"
            print "======================================"
            print " to display the token again, you may"
            print " run this script anytime"
    except IOError:
        print "Internet connection needed"
    except Exception, e:
        logging.exception('error')

if __name__ == '__main__':
    run()