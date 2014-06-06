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
        import urllib, constants, logging, os
        try:
            url = "http://"+constants.SERVER
            
            data = urllib.urlopen(url, self.toJson())
            response = json.dumps(data.read())
            if response['status'] == 'ok':
                print "sync complete deleting data"
                os.remove(open('monitor_data.p','wb'))

        except IOError:
            print "internet connection needed"
        except Exception,e:
            logging.exception("error")

    def toJson(self):
        return json.dumps([d.toJson() for d in self.data])