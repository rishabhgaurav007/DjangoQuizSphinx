from django.urls import path
from django.conf.urls import url, include
from .views import *
from . import views

app_name = 'subjective'


urlpatterns = [
    url(r'^$', view=IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', view=DetailView.as_view(), name='detail'),
    url(r'^#/$', view=views.first, name='first'),
    url(r'^checksub/$', views.checksubanswer, name='checksubanswer'),
    #url(r'^check/$', views.displayans, name='displayans'),
    url(r'^(?P<answer>[\w.]+)/submitscore/$', views.updatemarks, name='updatemarks'),
    url(r'^(?P<uas>[\w.@+-]+)$', views.displayans, name='displayans'),
    # path(r'^(?P<pk>[0-9]+)/submit/$', views.ques_ans, name='ques_ans'),
    #url(r'^(?P<ques_id>\d+)/submit/$', views.ques_ans, name='ques_ans'),
    url(r'^abc/submit/(?P<ques_id>\d+)$', views.ques_ans, name='ques_ans'),

]