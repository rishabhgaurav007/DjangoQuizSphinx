from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')), # This will include many urls like loin,logout
]