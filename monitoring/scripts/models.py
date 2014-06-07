# class file for the usage data
# @author ibaguio
import cPickle as pickle
import datetime, logging, json

class Usage(object):
    datetime = None
    load = [0,0,0] # 1,5,15 minute load ave
    uptime = None

    def __init__(self,uptime,load):
        self.datetime = datetime.datetime.now()
        self.uptime = uptime
        self.load = load
        print "Creating object"
        print "uptime",self.uptime
        print "load",self.load

    def toJson(self):
        return {"datetime":datetime.datetime.strftime(self.datetime,'%m/%d/%y %H:%M:%S'),
                "uptime":self.uptime,
                "load":self.load}

    @classmethod
    def create(cls,uptime_str):
        import re
        x_ = uptime_str.split('user')
        assert len(x_) == 2
        print x_[0]

        #uptime status
        uptime = x_[0].split()[2:-1]
        #TODO: take away trailing comma
        uptime = ' '.join(uptime) 

        #get the load
        p = re.compile('[a-zA-Z\ :,]')
        load = [x for x in p.split(x_[1]) if x]

        return Usage(uptime,load)

class UsageManager():
    data = []

    def __init__(self):
        self.loadData()

    def loadData(self):
        try:
            self.data = pickle.load(open('monitor_data.p','r'))
            print "data loaded",self.data
        except IOError,e:
            pass
        except Exception, e:
            logging.exception("error")

    def save(self):
        pickle.dump(self.data, open('monitor_data.p','wb'))

    def update(self,usage_data):
        print "updating usage",usage_data.toJson()
        self.data.append(usage_data)
        self.save()

    #sync to server
    def sync(self):
        import urllib, constants, logging, os, re, uuid
        try:
            url = "http://"+constants.SERVER+"/cgi/sync/"
            
            data_tosend = {"mac":':'.join(re.findall('..', '%012x' % uuid.getnode())),
                           "data": self.getData()}

            print "data_tosend",data_tosend
            data = urllib.urlopen(url,data=json.dumps(data_tosend))
            response = json.loads(data.read())
            print response
            if response['status'] == 'ok':
                print "sync complete deleting data"
                os.remove('monitor_data.p')

        except IOError:
            print "internet connection needed"
        except Exception,e:
            logging.exception("error")

    def getData(self):
        return [d.toJson() for d in self.data]

class TokenManager():
    token = ""

    def loadToken(self):
        try:
            self.token = pickle.load(open('token.p','r'))
        except Exception, e:
            logging.exception("error")
            raise e

    def save(self):
        pickle.dump(self.token, open('token.p','wb'))

    @classmethod
    def get_or_generate(cls):
        def randToken(len):
            import random
            return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(len))
        t = TokenManager()

        try:
            t.loadToken()

        except Exception, e:
            print "No token yet. Will create"
            t.token = randToken(5)
            t.save()
            print e

        return t.token