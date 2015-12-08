# coding: utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode

def index(request):
    return HttpResponse(u"<a href=astar>A* keresés</a><br><a href=minimax>minimax játékfa</a><br><a href=tests>tests</a>")