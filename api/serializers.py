from rest_framework import serializers
from webapp.models import *

class DeviceSerializer(serializers.ModelSerializer):
	user = serializers.Field(source='user.username')

	class Meta:
		model = Device
		fields = ('id', 'user', 'mac', 'device', 'model', 'os', 'dump')

class UsageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usage
		fields = ('id', 'device', 'datetime_received', 'datetime_sent', 'load', 'uptime')

class AnalyticsSerializer(serializers.ModelSerializer):
	user = serializers.Field(source='user.username')

	class Meta:
		model = Analytics
		fields = ('user', 'key', 'value')