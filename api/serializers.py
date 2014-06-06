from datetime import datetime, time, date, timedelta
from rest_framework import serializers
from webapp.models import *

class DeviceSerializer(serializers.ModelSerializer):
	user = serializers.Field(source='user.username')
	status = serializers.SerializerMethodField('getStatus')

	def getStatus(self, obj):
		buffertime = datetime.now() - timedelta(hours=1)
		usageinbuffer = obj.usage_set.filter(datetime__gt=buffertime)
		return "Tracking" if (usageinbuffer.count() > 0) else "Offline"

	class Meta:
		model = Device
		fields = ('id', 'user', 'status','mac', 'device', 'model', 'os', 'dump')

class UsageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usage
		fields = ('id', 'device', 'datetime', 'load', 'uptime')

class AnonymizedUsageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usage
		fields = ('datetime', 'load', 'uptime')		

class AnalyticsSerializer(serializers.ModelSerializer):
	user = serializers.Field(source='user.username')

	class Meta:
		model = Analytics
		fields = ('id', 'user', 'key', 'value')

class AnonymizedAnalyticsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Analytics
		fields = ('id', 'key', 'value')

class CustomGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomGroup
		fields = ('id', 'name')

class UserGroupSerializer(serializers.ModelSerializer):
	user = serializers.Field(source='user.username')
	group = serializers.Field(source='group.name')

	class Meta:
		model = UserGroup
		fields = ('id', 'user', 'group')

class GroupAnalyticsSerializer(serializers.ModelSerializer):
	group = serializers.Field(source='group.name')

	class Meta:
		model = GroupAnalytics
		fields = ('id', 'group', 'key', 'value')

class AnonymizedGroupAnalyticsSerializer(serializers.ModelSerializer):
	class Meta:
		model = GroupAnalytics
		fields = ('id', 'key', 'value')