# data crunching module
# @author ibaguio

from datetime import date, datetime, timedelta, time
from webapp.models import Usage
from django_facebook.models import FacebookCustomUser as User_
import json

def digest(date_=date.today()):
	#a and b are usage data
	def calc(a,b):
		if (a.datetime - b.datetime) < timedelta(minutes=6):
			load = int(json.loads(b.load)[1])
			wtg = b.device.consumption

			base_ = wtg * 0.4
			cons_ = base_ + ((load / b.device.cores) * (wtg - base_))

			return cons_

	def reduce_(data_set, uname):
		consumption = 0

		for i in range(1,len(data_set)):			
			c = calc(data_set[i-1],data_set[1])
			if c: 
				consumption += c

		print "consumption for",uname, consumption
		return consumption

	dtrange = (datetime.combine(date_, time.min),datetime.combine(date_, time.max))

	users = User_.objects.all()
	data = Usage.objects.filter(datetime__range=dtrange).order_by('-datetime')
	
	for user in users:
		for device in user.device_set.all():

			user_data = data.filter(device=device)
			reduce_(user_data, user.username)