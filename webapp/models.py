from django.db import models
from agila import settings

# Devices registered to user
class Device(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	mac = models.CharField(max_length=20)						
	device = models.CharField(max_length=100, null=True)		
	model = models.CharField(max_length=100, null=True)			
	os = models.CharField(max_length=100, null=True)			
	dump = models.TextField(null=True)

	class Meta:
		unique_together = ['user', 'mac']

	def __unicode__(self):
		return self.model

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
	datetime_received = models.DateTimeField(auto_now_add=True)
	datetime_sent = models.DateTimeField()
	load = models.CharField(max_length=100)
	uptime = models.CharField(max_length=20)