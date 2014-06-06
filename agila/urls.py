from django.conf.urls import patterns, include, url
from api import  views as api_views
from rest_framework.routers import DefaultRouter
from django.contrib import admin
admin.autodiscover()

api_router = DefaultRouter()
api_router.register(r'devices', api_views.DeviceViewSet, base_name='device')
api_router.register(r'usages', api_views.UsageViewSet, base_name='usage')
api_router.register(r'analytics', api_views.AnalyticsViewSet, base_name='analytics')

urlpatterns = patterns('',
	url(r'^api/', include(api_router.urls)),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook/', include('django_facebook.urls')),
	url(r'^accounts/', include('django_facebook.auth_urls')),

	url(r'^$', 'webapp.views.homepage', name='homepage'),
	url(r'^logout/', 'webapp.views.logout', name='logout'),
)
