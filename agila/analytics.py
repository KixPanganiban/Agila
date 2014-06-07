# data crunching module
# @author ibaguio

from datatime import date, datetime, timedelta, time
from webapp.models import Usage
from django_facebook import FacebookCustomUser as User_

def digest(date_=date.today()):
	def reduce(data_set):
		consumption = 0

	dtrange = (datetime.combine(date_, time.min),datetime.combine(date_, time.max))

	users = User_.objects.all()
	data = Usage.objects.filter(datetime__in_range=dtrange)
	
	for user in users:
		for device in user.device_set.all():

			user_data = data.filter(device=device)