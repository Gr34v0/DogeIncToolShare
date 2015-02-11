__author__ = 'Christian'

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib import messages

from django.contrib.auth.models import User

from users.forms import UserForm
from users.views import home

from users.models import BaseUser

def login(request):
    c = {}

    c.update(csrf(request))
    return render_to_response('DogeIncToolShare/login.html', c)


def auth_view(request):

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    args = {}

    if user is not None:
        auth.login(request, user)

        args['message'] = {'success': 'You have been logged in successfully'}
        args['activeuser'] = request.user
        return home(request, args)
        #return render_to_response("DogeIncToolShare/home.html", args)
    else:
        args['message'] = {'error': 'Invalid login details'}
        return home(request, args)
        #return render_to_response("DogeIncToolShare/home.html", args)

def logout(request):
    auth.logout(request)
    args = {}
    args['message'] = {'success': 'You have been logged out successfully'}
    return render_to_response('DogeIncToolShare/home.html', args)

def register_user(request):
    args = {}
    if request.method == 'POST':
        frm = UserForm(request.POST)

        if frm.is_valid():
            frm.save()
            args['message'] = {'success': 'Registered successfully'}
            return render_to_response('DogeIncToolShare/home.html', args)

    else:
        frm = UserForm()

    args['form'] = frm

    return render_to_response('DogeIncToolShare/register.html', args)

def page_does_not_exist(request):
    return render_to_response('DogeIncToolShare/404.html')
