from django.conf.urls import url

from AIQGen.views.index import index
from AIQGen.views.astar import astar
from AIQGen.views.minimax import minimax
from AIQGen.views.printview import printview
from AIQGen.views.test import testList, testCreate, testUpdate, testDelete
from AIQGen.views.problem import problemList, problemCreate, problemUpdate, problemDelete
from AIQGen.views.upload import upload



urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'astar', astar, name='astar'),
    url(r'minimax', minimax, name='minimax'),
    url(r'^printview/(?P<pk>\d+)$', printview, name='printview'),
    
    url(r'^tests$', testList, name='test_list'),
    url(r'^testnew$', testCreate, name='test_new'),
    url(r'^testedit/(?P<pk>\d+)$', testUpdate, name='test_edit'),
    url(r'^testdelete/(?P<pk>\d+)$', testDelete, name='test_delete'),

    url(r'^problems$', problemList, name='problem_list'),
    url(r'^problemnew$', problemCreate, name='problem_new'),
    url(r'^problemedit/(?P<pk>\d+)$', problemUpdate, name='problem_edit'),
    url(r'^problemdelete/(?P<pk>\d+)$', problemDelete, name='problem_delete'),

    url(r'^upload$', upload, name='upload'),
]
