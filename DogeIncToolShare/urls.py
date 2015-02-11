from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DogeIncToolShare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^community/', include('community.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^tools/', include('tools.urls')),
    url(r'^messaging/', include('messaging.urls')),

    url(r'^$', 'users.views.home', name='ToolShare'),
    url(r'^home', 'users.views.home', name='Home'),
    url(r'^community', 'community.views.viewCommunity', name='Community'),


    url(r'^users/login/$', 'DogeIncToolShare.views.login'),
    url(r'^users/auth/$', 'DogeIncToolShare.views.auth_view'),
    url(r'^users/logout/$', 'DogeIncToolShare.views.logout'),
    url(r'^users/loggedin/$', 'DogeIncToolShare.views.loggedin'),
    url(r'^users/invalid/$', 'DogeIncToolShare.views.invalid_login'),
    url(r'^users/register/$', 'DogeIncToolShare.views.register_user'),
    url(r'^users/register_success/$', 'DogeIncToolShare.views.register_success'),


    url(r'^404', 'DogeIncToolShare.views.page_does_not_exist'),

)
