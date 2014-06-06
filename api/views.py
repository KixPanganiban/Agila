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

class AnonymizedUsageViewSet(viewsets.ModelViewSet):
	queryset = Usage.objects.all()
	serializer_class = AnonymizedUsageSerializer

class AnalyticsViewSet(viewsets.ModelViewSet):
	serializer_class = AnalyticsSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Analytics.objects.all() if self.request.user.is_staff else Analytics.objects.filter(user=self.request.user)

class AnonymizedAnalyticsViewSet(viewsets.ModelViewSet):
	queryset = Analytics.objects.all()
	serializer_class = AnonymizedAnalyticsSerializer

class CustomGroupViewSet(viewsets.ModelViewSet):
	queryset = CustomGroup.objects.all()
	serializer_class = CustomGroupSerializer

class UserGroupViewSet(viewsets.ModelViewSet):
	serializer_class = UserGroupSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return UserGroup.objects.all() if self.request.user.is_staff else UserGroup.objects.filter(user=self.request.user)

class GroupAnalyticsViewSet(viewsets.ModelViewSet):
	serializer_class = GroupAnalyticsSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		groups = [group.id for group in UserGroup.objects.filter(user=self.request.user)]
		return GroupAnalytics.objects.all() if self.request.user.is_staff else GroupAnalytics.objects.filter(id__in=groups)

class AnonymizedGroupAnalyticsViewSet(viewsets.ModelViewSet):
	queryset = GroupAnalytics.objects.all()
	serializer_class = AnonymizedGroupAnalyticsSerializer

# API Entry Points
@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'devices': reverse('device-list', request=request, format=format),
		'usages': reverse('usage-list', request=request, format=format),
		'anonymizedusages': reverse('anonymizedusage-list', request=request, format=format),
		'anonymizedanalytics': reverse('anonymizedanalytics-list', request=request, format=format),
		'analytics': reverse('analytics-list', request=request, format=format),
		'customgroups': reverse('customgroup-list', request=request, format=format),
		'usergroups': reverse('usergroup-list', request=request, format=format),
		'anonymizedgroupanalytics': reverse('anonymizedgroupanalytics-list', request=request, format=format),
		'groupanalytics': reverse('groupanalytics-list', request=request, format=format),
		})