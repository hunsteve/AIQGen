from django.conf.urls import url

from AIQGen.views.index import index
from AIQGen.views.astar import astar
from AIQGen.views.minimax import minimax
from AIQGen.views.printview import testPrintView
from AIQGen.views.problemprintview import problemPrintView
from AIQGen.views.test import testList, testCreate, testUpdate, testDelete, testProblemList, testProblemRemove, testProblemAdd
from AIQGen.views.problem import problemList, problemCreate, problemUpdate, problemDelete, problemSelect
from AIQGen.views.upload import upload



urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'astar', astar, name='astar'),
    url(r'minimax', minimax, name='minimax'),
    url(r'^testprintview/(?P<pk>\d+)$', testPrintView, name='test_printview'),
    url(r'^problemprintview/(?P<pk>\d+)$', problemPrintView, name='problem_printview'),
    
    url(r'^tests$', testList, name='test_list'),
    url(r'^testnew$', testCreate, name='test_new'),
    url(r'^testedit/(?P<pk>\d+)$', testUpdate, name='test_edit'),
    url(r'^testdelete/(?P<pk>\d+)$', testDelete, name='test_delete'),
    url(r'^testproblemlist/(?P<pk>\d+)$', testProblemList, name='test_problem_list'),
    url(r'^testproblemremove/(?P<pk>\d+)$', testProblemRemove, name='test_problem_remove'),
    url(r'^testproblemadd/(?P<test_key>\d+)/(?P<problem_key>\d+)$', testProblemAdd, name='test_problem_add'),
    

    

    url(r'^problems$', problemList, name='problem_list'),
    url(r'^problemselect/(?P<test_key>\d+)$', problemSelect, name='problem_select'),
    url(r'^problemnew$', problemCreate, name='problem_new'),
    url(r'^problemnew/(?P<test_key>\d+)$', problemCreate, name='problem_new'),
    url(r'^problemedit/(?P<pk>\d+)$', problemUpdate, name='problem_edit'),
    url(r'^problemedit/(?P<pk>\d+)/(?P<test_key>\d+)$', problemUpdate, name='problem_edit'), 
    url(r'^problemdelete/(?P<pk>\d+)$', problemDelete, name='problem_delete'),

    url(r'^upload$', upload, name='upload'),
]
