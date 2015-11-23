 # coding: utf8
from django.shortcuts import render
from django.http import HttpResponse

def printview(request):
	return render(request, 'printview.html', {})