from django.conf.urls import patterns, include, url
from api import  views as api_views
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from agila import views
admin.autodiscover()

api_router = DefaultRouter()
api_router.register(r'devices', api_views.DeviceViewSet, base_name='device')
api_router.register(r'anonymizedusages', api_views.AnonymizedUsageViewSet, base_name='anonymizedusage')
api_router.register(r'usages', api_views.UsageViewSet, base_name='usage')
api_router.register(r'anonymizedanalytics', api_views.AnonymizedAnalyticsViewSet, base_name='anonymizedanalytics')
api_router.register(r'analytics', api_views.AnalyticsViewSet, base_name='analytics')
api_router.register(r'customgroups', api_views.CustomGroupViewSet, base_name='customgroup')
api_router.register(r'usergroups', api_views.UserGroupViewSet, base_name='usergroup')
api_router.register(r'anonymizedgroupanalytics', api_views.AnonymizedGroupAnalyticsViewSet, base_name='anonymizedgroupanalytics')
api_router.register(r'groupanalytics', api_views.GroupAnalyticsViewSet, base_name='groupanalytics')

urlpatterns = patterns('',
    url(r'^cgi/init/', views.firstuse),
    url(r'^cgi/sync/', views.status_update),
	url(r'^link/', 'webapp.views.link'),	
	url(r'^join_community/', 'webapp.views.join_community'),	

	url(r'^api/', include(api_router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook/', include('django_facebook.urls')),
	url(r'^accounts/', include('django_facebook.auth_urls')),

	url(r'^$', 'webapp.views.homepage', name='homepage'),
	url(r'^dashboard/', 'webapp.views.dashboard', name='dashboard')
)
