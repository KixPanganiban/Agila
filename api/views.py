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
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

	def get_queryset(self):
		queryset = Device.objects.all() if self.request.user.is_staff else Device.objects.filter(user=self.request.user)
		return queryset

class UsageViewSet(viewsets.ModelViewSet):
	queryset = Usage.objects.all()
	serializer_class = UsageSerializer

# API Entry Points
@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'devices': reverse('device-list', request=request, format=format),
		'usages': reverse('usage-list', request=request, format=format),
		})