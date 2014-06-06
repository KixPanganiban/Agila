from webapp.models import *
from api.serializers import *
from api.permissions import *
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, link
from rest_framework.reverse import reverse
from rest_framework.response import Response


# API Exit Points
class DeviceViewSet(viewsets.ModelViewSet):
	serializer_class = DeviceSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Device.objects.all() if self.request.user.is_staff else Device.objects.filter(user=self.request.user)

class UsageViewSet(viewsets.ModelViewSet):
	serializer_class = UsageSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Usage.objects.all() if self.request.user.is_staff else Usage.objects.filter(device__in=self.request.user.device_set.all())


class AnalyticsViewSet(viewsets.ModelViewSet):
	serializer_class = DeviceSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Analytics.objects.all() if self.request.user.is_staff else Analytics.objects.filter(user=self.request.user)

# API Entry Points
@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'devices': reverse('device-list', request=request, format=format),
		'usages': reverse('usage-list', request=request, format=format),
		'analytics': reverse('analytics-list', request=request, format=format),
		})