__author__ = 'Christian'

from django.conf.urls import patterns, url
from messaging import views

urlpatterns = patterns('',
           url(r'inbox/', views.inbox, name='Inbox'),
           url(r'sentMessages/', views.sentMessages, name='Sent Mail'),
           url(r'sendMessage/', views.sendMessage, name='Sending Message'),
           url(r'^(?P<message_id>\d+)/$', views.viewMessage, name='Message ^(?P<message_id>\d+)/$'),
)
