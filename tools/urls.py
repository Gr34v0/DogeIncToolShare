from django.conf.urls import patterns, url

from tools import views

urlpatterns = patterns('',
    url(r'display_tools/', views.display_tools),
    url(r'tool_register/', views.tool_register, name='tool_register'),
    url(r'browse_tools/', views.browse_tools, name='browse_tools'),                   
    url(r'^search/$', views.search, name='search'),
    url(r'tool_manage/', views.tool_management, name='tool_management'),
    url(r'^(?P<tool_id>\d+)/$', views.view_tool, name='view_tool'),
    url(r'^borrow/(?P<tool_id>\d+)/$', views.borrow_tool, name='borrow_tool'),
    url(r'^request_edit/(?P<tool_request_id>\d+)/$', views.edit_tool_request, name='edit_request'),
    url(r'^borrow/(?P<tool_id>\d+)/(?P<receiver_id>\d+)/$', views.send_tool_request, name='send_tool_request'),                   
    url(r'^return/(?P<tool_id>\d+)/$', views.return_tool, name='return_tool'),
    url(r'^tool_edit/(?P<tool_id>\d+)/$', views.tool_edit, name='tool_edit'),
)
