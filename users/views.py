from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from .forms import *
from django.core.context_processors import csrf

from .models import BaseUser

# Create your views here.

def home(request, args = None):
    """ Function to call the Home page from the site

    :param request: The HTTP request handled by Django
    :param args: args associated with the page rendering
    :return: a render_to_response call for the home.html page and passed args set
            args will either be empty or contain the activeuser
    """

    if args is None:
        args = {}

    if request.user.is_active:
        args['activeuser'] = request.user

    return render_to_response("DogeIncToolShare/home.html", args)


@login_required(login_url='/home/')
def userProfile(request):
    """ Fucntion to call the user profile management page

    :param request: The HTTP request handled by Django
    :return: a render_to_response call for the profile.html page and passed args set if the method is GET
            or an HttpResponseRedirect to the /home/ url if the method is POST

            args contains a form object
    """

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save() #Details have been updated to the database
            return HttpResponseRedirect('/home/')

    elif request.method == 'GET':
        profile = request.user
        form = UserUpdateForm(initial={'first_name': profile.first_name,
                                        'last_name': profile.last_name,
                                        'email': profile.email,
                                        'zipcode': profile.zipcode,
                                        'address': profile.address,
        })

    args = {}
    args['form'] = form
    if request.user.is_active:
        args['activeuser'] = request.user

    return render_to_response('DogeIncToolShare/profile.html', args)


@login_required(login_url='/home/')
def userSecurity(request):
    """ Fucntion to call the user profile security management page; very similar to the userProfile() function

    :param request: The HTTP request handled by Django
    :return: a render_to_response call for the security.html page if the method is GET
            or a HttpResponseRedirect for the /home/ url if the method is POST

            args contains a form object
    """

    if request.method == 'POST':
        form = UserSecurityForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save() #Details have been updated to the database
            return HttpResponseRedirect('/home/')

    elif request.method == 'GET':
        profile = request.user
        form = UserSecurityForm(initial={'username': profile.username,
        })

    args = {}
    args['form'] = form
    if request.user.is_active:
        args['activeuser'] = request.user

    return render_to_response('DogeIncToolShare/security.html', args)