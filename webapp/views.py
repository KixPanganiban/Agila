from django.shortcuts import render, redirect, render_to_response
import django_facebook

def homepage(request):
	return render(request, "homepage.html")

def dashboard(request):
	return render(request, "dashboard.html")