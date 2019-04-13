from django.conf.urls import url
from .views import *
from . import views
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
app_name = 'quiz'


urlpatterns = [
    url(r'^leaderboard/$', views.LeaderBoard, name='leaderboard'),
    url(r'^$', view=index, name='index'),
    url(r'^quizzes/$', view=QuizListView.as_view(), name='quiz_index'),
    path('progress/', views.ProgressView, name='progress'),

    url(r'^category/$', view=CategoriesListView.as_view(), name='quiz_category_list_all'),
    url(r'^category/(?P<category_name>[\w|\W-]+)/$', view=ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'),
    url(regex=r'^(?P<quiz_name>[\w-]+)/take/$',view=QuizTake.as_view(), name='quiz_question'),
    #url(regex=r'^(?P<quiz_name>[\w-]+)/subtake/$',view=QuizSubTake.as_view(), name='quiz_question_sub'),
    #url(regex=r'^(?P<pk>[0-9]+)/subtake/$',view=QuizSubTake.as_view(), name='quiz_question_sub'),
    #path('', include('authenticate.urls')),
    #url(r'^(?P<ques_id>\d+)/submit/$', views.ques_ans, name='ques_ans'),
    #path(regex=r'^(?P<quiz_name>[\w-]+)/subtake/$', include('subjective.urls')),
]