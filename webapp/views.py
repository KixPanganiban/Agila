from datetime import datetime, time, timedelta
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from models import *
import django_facebook

def homepage(request):
	return render(request, "homepage.html")

@login_required(login_url='/')
def dashboard(request):
	devices = request.user.device_set.all()
	groups = request.user.usergroup_set.all()

	# Put string data
	for device in devices:
		buffertime = datetime.now() - timedelta(hours=1)
		usageinbuffer = device.usage_set.filter(datetime__gt=buffertime)
		device.status = "Tracking" if (usageinbuffer.count() > 0) else "Offline"
		device.statusclass = "label-success" if (usageinbuffer.count() > 0) else "label-danger"

	return render(request, "dashboard.html", {
		"devices": devices,
		"groups": groups
		})