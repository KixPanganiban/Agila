from django.conf.urls import patterns, include, url

from django.contrib import admin
from agila import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^cgi/init/', views.firstuse),
    url(r'^cgi/sync/', views.status_update),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook/', include('django_facebook.urls')),
	url(r'^accounts/', include('django_facebook.auth_urls')),
	url(r'^$', 'webapp.views.homepage', name='homepage'),
	url(r'^logout/', 'webapp.views.logout', name='logout'),
)
