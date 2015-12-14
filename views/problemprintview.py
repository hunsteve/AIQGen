 # coding: utf8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from AIQGen.models import Test, Problem, ProblemInTest


def problemPrintView(request, pk):
    problem = get_object_or_404(Problem, pk=pk)    
    return render(request, 'problemprintview.html', {'question':{'body':problem.text, 'score':problem.score, 'index':1, 'freespace':0 }})
