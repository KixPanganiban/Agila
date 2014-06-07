from webapp.models import Device, DeviceToken, Usage
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json, logging

@require_POST
@csrf_exempt
def firstuse(request):
	data = request.POST
	print data
	try:
		vars = ['os', 'mac', 'token', 'cores']
		for var in vars: 
			if var not in data: return HttpResponse(json.dumps({"status":"error"}))

		return HttpResponse(json.dumps({"status":"ok"})) if Device.createWithToken(data['token'], data['mac'], data['os'], data['cores']) else HttpResponse(json.dumps({"status": "fail"}))

	except Exception, e:
		logging.exception("error")
		return HttpResponse(json.dumps({"status":"invalid"}))

	return HttpResponse(json.dumps({"status":"error"}))

@require_POST
@csrf_exempt
def status_update(request):
	import logging
	try:
		data = json.loads(request.body)
		mac = data['mac']
		for d in data['data']:
			if Usage.create(d,mac):
				continue
			return HttpResponse(json.dumps({"status":"error"}))

		return HttpResponse(json.dumps({"status":"ok"}))

	except Exception, e:
		logging.exception("error")

	return HttpResponse(json.dumps({"status":"error"}))