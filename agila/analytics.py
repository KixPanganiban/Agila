# data crunching module
# @author ibaguio

from datetime import date, datetime, timedelta, time
from webapp.models import Usage, Analytics, UserRanking
from django_facebook.models import FacebookCustomUser as User_
import json

def digest(date_=date.today()):
	#a and b are usage data
	#consumption is in WH 
	def calc(a,b):
		if (a.datetime - b.datetime) < timedelta(minutes=6):
			load = float(b.load.split(",")[1])
			wtg = b.device.consumption

			base_ = wtg * 0.4 
			cons_ = base_ + ((load / b.device.cores) * (wtg - base_))
			return cons_ * ( 5/60.0)

	def reduce_(data_set, uname):
		consumption = 0
		for i in range(1,len(data_set)):
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

# consumption is in wattage
def user_consumption_total(user, date_=date.today(), days_=None):
	total_ = Analytics.objects.filter(user=user,key="consumption")

	if days_:
		dtrange = (datetime.combine(date_-timedelta(days=days_), time.min),datetime.combine(date_, time.max))
		total_ = total_.filter(date__range=dtrange)
	cons = 0

	for i in total_:
		cons += float(i.value)

	return cons

def user_consumption_range(user, date_start, date_end):
	dtrange = (datetime.combine(date_start, time.min),datetime.combine(date_end, time.max))

	days_ = date_end - date_start
	daily_cons = []
	for i in range(days_):
		data = Analytics.objects.filter(user=user,key="consumption",date=date_start+timedelta(days=i))
		cons_ = 0
		for d in data:
			cons_ += float(d.value)
		daily_cons.append(cons)

	return daily_cons

def group_consumption_total(group, date_=date.today(), days_=None):
	users  = [usr.user for usr in UserGroup.objects.filter(group=group).all()]
	total_ = Analytics.objects.filter(user__in=[users],key="consumption")

	if days_:
		dtrange = (datetime.combine(date_-timedelta(days=days_), time.min),datetime.combine(date_, time.max))
		total_ = total_.filter(date__range=dtrange)
	cons = 0

	for i in total_:
		cons += float(i.value)

	return cons

def user_percentile(user, date_=date.today(), days_=None):
	UserRanking.getRank(date_,days_)
	rank = UserRanking.objects.get(user=user)
	total = UserRanking.objects.all().count()

	return rank.rank / float(total)

def group_percentile(group, date_=date.today(), days_=None):
	GroupRanking.rank(date_,days_)
	rank = GroupRanking.objects.get(group=group)
	total = GroupRanking.objects.count()

	return rank / float(total)

def user_leaderboard(display=10):
	return [user for user in UserRanking.objects.order_by('rank')[:display]]

def group_leaderboard(display=10):
	return [group for group in GroupRanking.objects.order_by('rank')[:display]]

def user_consumption_wrt_group(user, group, date_=date.today(), days_=None):
	g = group_consumption_total(group, date_=date_, days_=days_)
	u = user_consumption_total(user, date_=date_, days_=days_)

	return (u / g) * 100