from datetime import datetime, time, timedelta
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from models import *
import django_facebook
import json

def getFlash(request):
	if 'flash' in request.session and request.session['flash']:
		flash = request.session.get('flash')
		request.session['flash'] = None
		return flash
	else:
		return None

def storeFlash(request, message, type):
	request.session['flash'] = { "message": message, "type": type }
	return True

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
		groups_json = json.dumps([group.name for group in CustomGroup.objects.all()])

	return render(request, "dashboard-main.html", {
		"devices": devices,
		"groups": groups,
		"flash": getFlash(request),
		"groups_json": groups_json
		})

@login_required(login_url='/')
def link(request):
	code = request.POST.get("code")
	if Device.activate(code, request.user):
		storeFlash(request, "Your device has been successfully linked!", "success")
	else:
		storeFlash(request, "Unable to link device. Please check if you have the right token!", "danger")
	return redirect("/dashboard/")

@login_required(login_url='/')
def join_community(request):
	community = request.POST.get("community")

	if len(community) < 1:
		storeFlash(request, "Can't join a blank community, sorry. Please enter a name.", "info")
		return redirect('/dashboard/')

	groups = CustomGroup.objects.filter(name__iexact=community)
	if (groups.count() > 0):
		group = groups.get()
		try:
			new_usergroup = UserGroup(user=request.user, group=group)
			new_usergroup.save()
		except Exception, e:
			print e
			storeFlash(request, "You are unable to join that group.", "danger")
	else:
		with transaction.atomic():
			try:
				new_group = CustomGroup(name=community)
				new_group.save()
				new_usergroup = UserGroup(user=request.user, group=new_group)
				new_usergroup.save()
			except Exception, e:
				storeFlash(request, "You are unable to join that group.", "danger")

	storeFlash(request, "You successfully joined %s!"%(community), "success")
	return redirect('/dashboard/')
