from django.shortcuts import render, redirect, render_to_response

def homepage(request):
	return render(request, "base.html")