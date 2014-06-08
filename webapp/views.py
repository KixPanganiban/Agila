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
	devices = request.user.device_set.filter(linked=True)
	groups = request.user.usergroup_set.all()
	appdb = AppDB.objects.filter(type='DUMB')
	dumbapps = request.user.dumbdevice_set.filter(linked=True)
	hours = [
		{"value": 0, "text": "12am"},
		{"value": 1, "text": "1am"},
		{"value": 2, "text": "2am"},
		{"value": 3, "text": "3am"},
		{"value": 4, "text": "4am"},
		{"value": 5, "text": "5am"},
		{"value": 6, "text": "6am"},
		{"value": 7, "text": "7am"},
		{"value": 8, "text": "8am"},
		{"value": 9, "text": "9am"},
		{"value": 10, "text": "10am"},
		{"value": 11, "text": "11am"},
		{"value": 12, "text": "12pm"},
		{"value": 13, "text": "1pm"},
		{"value": 14, "text": "2pm"},
		{"value": 15, "text": "3pm"},
		{"value": 16, "text": "4pm"},
		{"value": 17, "text": "5pm"},
		{"value": 18, "text": "6pm"},
		{"value": 19, "text": "7pm"},
		{"value": 20, "text": "8pm"},
		{"value": 21, "text": "9pm"},
		{"value": 22, "text": "10pm"},
		{"value": 23, "text": "1pm"}
	]

	from agila.analytics import user_consumption_total as uct
	from agila.analytics import user_percentile as upercentile
	user_consumption = uct(request.user)
	user_consumption_today = uct(user=request.user, days_=1)
	user_percentile = upercentile(request.user)

	consumption_not_set = 0

	# Put string data
	for device in devices:
		if not device.consumption:
			device.status = "Set Wattage"
			device.statusclass = "label-warning"
			consumption_not_set += 1
		else:
			buffertime = datetime.now() - timedelta(hours=1)
			usageinbuffer = device.usage_set.filter(datetime__gt=buffertime)
			device.status = "Tracking" if (usageinbuffer.count() > 0) else "Offline"
			device.statusclass = "label-success" if (usageinbuffer.count() > 0) else "label-danger"

	for group_ in groups:
		group_.members = group_.group.members if group_.group.members else 0
	
	groups_json = json.dumps([group.name for group in CustomGroup.objects.all()])

	return render(request, "dashboard-main.html", {
		"user_consumption": user_consumption,
		"user_consumption_today": user_consumption_today,
		"user_percentile": user_percentile,
		"devices": devices,
		"groups": groups,
		"flash": getFlash(request),
		"groups_json": groups_json,
		"appdb": appdb,
		"dumbapps": dumbapps,
		"days": ['Su', 'M', 'T', 'W', 'Th', 'Fr', 'Sa'],
		"hours": hours,
		"setconsumption": True if consumption_not_set > 0 else False
		})

@login_required(login_url='/')
def analytics(request):
	groups = request.user.usergroup_set.all()
	return render(request, "dashboard-analytics.html", {
		"groups": groups
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
def unlink(request):
	if 'id' not in request.GET:
		return redirect('/dashboard/')
	id = request.GET.get('id')
	try:
		device = Device.objects.get(id=id)
		device.linked = False
		device.user = None
		device.save()
	except Exception, e:
		print e
		storeFlash(request, "Something went wrong. We can't unlink your device. Please try again.", "danger")
		return redirect('/dashboard/')

	storeFlash(request, "Device unlinked! You can link again anytime.", "success")
	return redirect('/dashboard/')

@login_required(login_url='/')
def join_community(request):
	community = request.POST.get("community")

	if len(community) < 1:
		storeFlash(request, "Can't join a blank community, sorry. Please enter a name.", "info")
		return redirect('/dashboard/')

	groups = CustomGroup.objects.filter(name__iexact=community)
	if (groups.count() > 0):
		group = groups.get()
		
		user_groups = request.user.usergroup_set.all()
		if group in user_groups:
			storeFlash(request, "You're already a member of that group!", "warning")
			return redirect('/dashboard/')

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

@login_required(login_url='/')
def leave_community(request):
	if 'id' not in request.GET:
		return redirect('/dashboard/')

	community_id = request.GET.get('id')
	try:
		community_link = UserGroup.objects.get(id=community_id)
		community_name = community_link.group.name
		community_link.delete()
	except Exception, e:
		print e
		storeFlash(request, "Unable to remove you from that community.", "danger")
		return redirect("/dashboard/")

	storeFlash(request, "You have successfully left %s."%community_name, "success")
	return redirect('/dashboard/')

@login_required(login_url='/')
def appdb(request):
	if request.method == "GET":
		appdb = AppDB.objects.all()
		for app in appdb:
			app.typestring = "Smart Device" if app.type is "SMART" else "Non-Smart Appliance"
		return render(request, "appdb.html", {
			"flash": getFlash(request),
			"appdb": appdb
			})
	else:
		for x in ["name", "wattage"]:
			if x not in request.POST:
				storeFlash(request, "Unable to submit device, you need to fill in all the details.", "danger")
				return redirect('/appdb/')
		try:
			new_device = AppDB(
				name = request.POST.get('name'),
				wattage = int(request.POST.get('wattage')),
				type = "SMART" if request.POST.get('is_smart') else "DUMB")
			new_device.save()
		except Exception, e:
			print e
			storeFlash(request, "Unable to submit device, something went wrong!", "danger")
			return redirect('/appdb/')

	storeFlash(request, "Your application has been submitted! Thanks!", "success")
	return redirect('/appdb/')

@login_required(login_url="/")
def add_appliance(request):
	description = request.POST.get('description')
	appdb = AppDB.objects.get(id=request.POST.get('class'))
	schedule = ""
	for x in ['Su', 'M', 'T', 'W', 'Th', 'Fr', 'Sa']:		
		schedule += '1' if "day-"+x in request.POST else '0'
	for x in xrange(1, 25):
		schedule += '1' if "hour-"+str(x) in request.POST else '0'

	try:
		new_dumbdevice = DumbDevice(
			user=request.user,
			appdb=appdb,
			description=description,
			schedule=schedule,
			linked=True)
		new_dumbdevice.save()
	except Exception, e:
		print e
		storeFlash(request, 'Something went wrong. We can\'t save that appliance.', 'danger')
		return redirect('/dashboard/')

	storeFlash(request, 'Your appliance has been added! Thanks!', 'success')
	return redirect('/dashboard/')

@login_required(login_url='/')
def set_wattage(request):
	for x in ['id', 'set-wattage']: 
		if x not in request.POST:
			print "not found ", x
			storeFlash(request, "Something went wrong with your request, please try again.", "danger")
			return redirect('/dashboard/')

		try:
			device = Device.objects.get(id=request.POST.get('id'))
			device.consumption = request.POST.get('wattage')
			device.save()
		except Exception, e:
			print e
			storeFlash(request, "Something went wrong with your request, please try again.", "danger")
			return redirect('/dashboard/')
		storeFlash(request, "Wattage set. Thanks!", "success")
		return redirect('/dashboard/')
