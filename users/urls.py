__author__ = 'Christian'

from django.conf.urls import patterns, url
from users import views


urlpatterns = patterns('',
    url(r'profile/', views.userProfile, name='User Profile'),
    url(r'security/', views.userSecurity, name='User Security')
)