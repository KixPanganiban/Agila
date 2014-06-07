# data crunching module
# @author ibaguio

from datetime import date, datetime, timedelta, time
from webapp.models import Usage, Analytics
from django_facebook.models import FacebookCustomUser as User_
import json

def digest(date_=date.today()):
	#a and b are usage data
	def calc(a,b):
		if (a.datetime - b.datetime) < timedelta(minutes=6):
			load = float(b.load.split(",")[1])
			wtg = b.device.consumption

			base_ = wtg * 0.4 
			print "wtg",wtg
			print "base",base_
			print "load",load
			print "cores",b.device.cores
			print "wtf - base", (wtg - base_)
			cons_ = base_ + ((load / b.device.cores) * (wtg - base_))
			print "cons",cons_
			print "a",cons_ * ( 5/60.0 )
			return cons_ * ( 5/60.0)

	def reduce_(data_set, uname):
		consumption = 0
		print "Data set",data_set
		for i in range(1,len(data_set)):
			print "i",data_set[i]
			print "i-1",data_set[i-1]
			c = calc(data_set[i-1],data_set[i])
			if c: 
				consumption += c
		print "consumption for",uname, consumption
		return consumption

	dtrange = (datetime.combine(date_, time.min),datetime.combine(date_, time.max))

	users = User_.objects.all()
	data = Usage.objects.filter(datetime__range=dtrange).order_by('-datetime')
	
	for user in users:
		print "digesting",user
		for device in user.device_set.all():
			print "digesting",str(user)+"'s",device
			user_data = data.filter(device=device)
			cons = reduce_(user_data, user.username)

			Analytics.updateConsumption(user,device,date_,cons)

def user_data_json(user):
	j = []
	print user.device_set.all()
	for device in user.device_set.all():
		j.append({"mac":device.mac,
		 		  "daily_consumption":[ {"date": dev_data.date,
		                        "consumption": dev_data.value} for dev_data in device.analytics_set.all()\
		                        	if dev_data.key == 'consumption' ]})
	return j