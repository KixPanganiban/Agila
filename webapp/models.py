from django.db import models, transaction
from agila import settings

# Devices registered to user
class Device(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	mac = models.CharField(max_length=20)						
	device = models.CharField(max_length=100, null=True, blank=True)
	model = models.CharField(max_length=100, null=True, blank=True)		
	os = models.CharField(max_length=100, null=True, blank=True)		
	dump = models.TextField(null=True, blank=True)

	class Meta:
		unique_together = ['user', 'mac']

	def __unicode__(self):
		return self.mac

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
					device = cls.objects.get(mac=mac)
					device.user = user
					device.save()
				except Exception, e:
					print e
					return False

				return True
			else:
				return False

	@classmethod
	def createWithToken(cls, token, mac, os, dump=None):
		with transaction.atomic():
			newdevice = cls(user=None, mac=mac, device=None, model=None, os=os, dump=dump)
			newdevice.save()

			newtoken = DeviceToken(token=token, mac=mac)
			newtoken.save()


class DeviceToken(models.Model):
	token = models.CharField(max_length=6,unique=True)
	mac = models.CharField(max_length=20, null=True)

# Using CustomGroup because actual Group is already used by Django.auth
class CustomGroup(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name

# Surrogate table to link auth.User object with CustomGroup
class UserGroup(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	group = models.ForeignKey(CustomGroup)

	class Meta:
		unique_together = ['user', 'group']

	def __unicode__(self):
		return "[%s] %s"%(self.group.name, self.user.username)

# Variable-form table for user analytics
class Analytics(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	date = models.DateField(auto_now_add=100)

	class Meta:
		unique_together = ['user', 'key']

	def __unicode__(self):
		"%s (%s)"%(self.user.username, self.key)

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
		import datetime, logging
		try:
			device = Device.objects.get(mac=mac)
			u = Usage(device=device, datetime=datetime.datetime.strptime(data['datetime'],"%m/%d/%y %H:%M:%S"),
				load=data['load'],uptime=data['uptime'])
			u.save()
			return True
		except Exception, e:
			logging.exception("error")
