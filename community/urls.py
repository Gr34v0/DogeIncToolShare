__author__ = 'Shalimar'

from django.conf.urls import patterns, url
from community import views


urlpatterns = patterns('',
    url(r'join/', views.joinCommunity, name='Join Community'),
    url(r'register/', views.registerCommunity, name='Register Community'),
    url(r'admin/accept/(?P<user_id>\d+)/', views.acceptUser, name='Accept User'),
    url(r'admin/deny/(?P<user_id>\d+)/', views.denyUser, name='Deny User'),
)
