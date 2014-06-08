from django.db import models, transaction
from agila import settings
from django_facebook.models import FacebookCustomUser as User_
from datetime import date, timedelta
# Devices registered to user
class Device(models.Model):
	user = models.ForeignKey(User_, null=True)
	mac = models.CharField(max_length=20)						
	device = models.CharField(max_length=100, null=True,blank=True)
	model = models.CharField(max_length=100, null=True,blank=True)		
	os = models.CharField(max_length=100, null=True,blank=True)		
	cores = models.IntegerField(null=False,blank=True, default=1)
	consumption = models.IntegerField(null=True)
	linked = models.BooleanField(default=True)

	class Meta:
		unique_together = ['user', 'mac']

	def __unicode__(self):
		if self.user:
			return "%s %s"%(self.user.username, self.mac)
		else:
			return "UNLINKED %s"%(self.mac)

	@classmethod
	def activate(cls, token, user):
		with transaction.atomic():
			if DeviceToken.objects.filter(token=token).count() > 0:
				try:
					dt = DeviceToken.objects.get(token=token)
					mac = dt.mac
					dt.delete()
				except Exception, e:
					print e
					return False

				try:
					device = cls.objects.exclude(linked=False).get(mac=mac)
					device.user = user
					device.save()
				except Exception, e:
					print e
					return False

				return True
			else:
				return False

	@classmethod
	def createWithToken(cls, token, mac, os,cores, dump=None):
		with transaction.atomic():
			newdevice = cls(user=None, mac=mac, device=None, model=None, os=os, cores=cores, linked=True)
			newdevice.save()

			newtoken = DeviceToken(token=token, mac=mac)
			newtoken.save()


class DeviceToken(models.Model):
	token = models.CharField(max_length=6,unique=True)
	mac = models.CharField(max_length=20, null=True)

	def __unicode__(self):
		try:
			user = Device.objects.get(mac=self.mac).user.username
			return "%s %s"%(self.user, self.mac)
		except:
			return self.mac

# Also called the AppDB, for devices with non-smart capabilities
class AppDB(models.Model):
	name = models.CharField(max_length=100)
	wattage = models.IntegerField()		# If smart device, this translates to consumption
	type = models.CharField(max_length=100, choices=[['DUMB', 'DUMB'], ['SMART', 'SMART']])

	def __unicode(self):
		return "%s wH %s"%(self.wattage, self.name)

class DumbDevice(models.Model):
	user = models.ForeignKey(User_, null=True)
	description = models.TextField(null=True)
	appdb = models.ForeignKey(AppDB, null=True)
	schedule = models.CharField(max_length=32, default="".join(['0' for x in xrange(32)]))
	linked = models.BooleanField(default=True)

	def __unicode__(self):
		return "%s wH %s"%(self.appdb.wattage, self.description)

# Using CustomGroup because actual Group is already used by Django.auth
class CustomGroup(models.Model):
	name = models.CharField(max_length=100, unique=True)
	members = models.IntegerField(null=True)		# Auto-updated every time a new UserGroup is made

	def __unicode__(self):
		return self.name

# Surrogate table to link auth.User object with CustomGroup
class UserGroup(models.Model):
	user = models.ForeignKey(User_)
	group = models.ForeignKey(CustomGroup)

	class Meta:
		unique_together = ['user', 'group']

	# Add 1 to CustomGroup members every time 1 joins
	def save(self, *args, **kwargs):
		if not self.group.members: self.group.members = 0
		self.group.members += 1
		self.group.save()
		super(UserGroup, self).save(*args, **kwargs)

	# Remove 1 to CustomGroup members every time 1 leaves
	def delete(self, *args, **kwargs):
		if not self.group.members: self.group.members = 1
		self.group.members -= 1
		self.group.save()
		super(UserGroup, self).save(*args, **kwargs)

	def __unicode__(self):
		return "[%s] %s"%(self.group.name, self.user.username)

# Variable-form table for user analytics
class Analytics(models.Model):
	user = models.ForeignKey(User_)
	device = models.ForeignKey(Device, null=True)
	dumbdevice = models.ForeignKey(DumbDevice, null=True)
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	date = models.DateField(auto_now_add=100)

	class Meta:
		unique_together = ['user', 'key']

	def __unicode__(self):
		return "%s %s: %s"%(self.user.username, self.key, self.value)

	@classmethod
	def updateConsumption(cls, user, device, date, cons):
		try:
			a = Analytics(user=user,device=device, key="consumption", value=str(cons), date=date)
			a.save()
		except Exception, e:
			print e
			raise e

	@classmethod
	def getPrice(self, date, user, device=None):
		if self.key != "consumption": return
		price = 12.66 / 1000

		data = Analytics.objects.filter(user=user,date=date)
		if device:
			data = data.filter(device=device)

		sum_ = 0
		for d in data: sum_ += float(d)
		return sum_

	def getPrice(self):
		if self.key != "consumption":
			return
		price = 12.66 / 1000
		return float(self.value) * price

# Variable-form table for group analytics
class GroupAnalytics(models.Model):
	group = models.ForeignKey(CustomGroup)
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)

	class Meta:
		unique_together = ['group', 'key']

	def __unicode__(self):
		"%s (%s)"%(self.group.name, self.key)

# Usage statistics gathered from heartbeat
class Usage(models.Model):
	device = models.ForeignKey(Device)
	datetime = models.DateTimeField()
	load = models.CharField(max_length=100)
	uptime = models.CharField(max_length=20)

	def __unicode__(self):
		return "%s %s %s"%(self.device.user.username, self.load, self.datetime)

	@classmethod
	def create(cls,data,mac):
		import datetime, logging, json
		try:
			device = Device.objects.get(mac=mac)
			load = ','.join(data['load'])
			u = Usage(device=device, datetime=datetime.datetime.strptime(data['datetime'],"%m/%d/%y %H:%M:%S"),
				load=load,uptime=data['uptime'])
			u.save()
			return True
		except Exception, e:
			logging.exception("error")

class UserRanking(models.Model):
	user = models.ForeignKey(User_,unique=True)
	rank = models.IntegerField()
	
	@classmethod
	def add_or_update(cls, user, rank_):
		u = cls.objects.filter(user=user)
		if u.count() == 1:
			u = u.get()
			u.rank = rank_
			u.save()
		else:
			u = cls(user, rank_)
			u.save()

	@classmethod
	def rank(cls, date_=date.today(), days=30):
		from agila.analytics import user_consumption_total
		users = User_.objects.all()
		
		rankng = []

		for user in users:
			cons = user_consumption_total(user, date_=date_, days_=days)
			rankng.append((user,cons))
		
		rankng = sorted(rankng, key= lambda score: score[1])

		for i in range(len(rankng)):
			user = rankng[i][0]
			UserRanking.add_or_update(user,i+1)

class GroupRanking(models.Model):
	group = models.ForeignKey(CustomGroup,unique=True)
	rank = models.IntegerField()
	
	@classmethod
	def add_or_update(cls, group, rank):
		u = GroupRanking.objects.filter(group=group)
		if u.count() == 1:
			u = u.get()
			u.rank = rank
			u.save()
		else:
			u = GroupRanking(group, rank)
			u.save()

	@classmethod
	def rank(cls, date_=date.today(), days=30):
		from analytics import group_consumption_total
		groups = User_.objects.all()
		
		rankng = []

		for group in groups:
			cons = group_consumption_total(group, date_=date_, days_=days)
			rankng.append((group,cons))
		
		rankng = sorted(rankng, key= lambda score: score[1])

		for i in range(len(rankng)):
			r = rankng[i]
			GroupRanking.add_or_update(r[0],i+1)
