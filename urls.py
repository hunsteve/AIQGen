from django.conf.urls import url

from AIQGen.views.index import index
from AIQGen.views.astar import astar
from AIQGen.views.minimax import minimax
from AIQGen.views.printview import printview



urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'astar', astar, name='astar'),
    url(r'minimax', minimax, name='minimax'),
    url(r'printview', printview, name='printview'),
]
