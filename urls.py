from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'astar', views.astar, name='astar'),
    url(r'minimax', views.minimax, name='minimax'),
]
