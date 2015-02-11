from django.shortcuts import render
from .models import Message
from .forms import MessageForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/home/')
def inbox(request):
    """  Function to call the inbox page from the site

    :param request: the HTTP request handled by Django
    :return: a render_to_response call for the inbox.html page and passed args set

            args will contain messages with a to_user being the active user
    """

    args = {}

    args['messages'] = Message.objects.filter(to_user = request.user.id)

    if request.user.is_active:
        args['activeuser'] = request.user

    return render_to_response('messaging/inbox.html', args)



@login_required(login_url='/home/')
def sendMessage(request):
    """ Function to call the send message page

    :param request: the HTTP request handled by Django
    :return: calls the inbox method with a passed in args set containing a success notification if the method is POST
            or a render_to_response for the send_message.html page and passed args set if the method is GET

            args contains a form object
    """
    if request.method == 'POST':

        frm = MessageForm(request.POST)
        if frm.is_valid():
            frm.save()
            return HttpResponseRedirect('/inbox/')


    elif request.method == 'GET':
        return



@login_required(login_url='/home/')
def sentMessages(request):
    """ Funtion to call the outbox page

    :param request: the HTTP request handled by Django
    :return: a render_to_response call for the outbox.html page and the passed args set

            args contains all messages with from_user being the active user.
    """

    if request.method == 'GET':

        args = {}

        args['messages'] = Message.objects.filter(from_user = request.user.id)

        if request.user.is_active:
            args['activeuser'] = request.user

        return render_to_response('messaging/sentMessages.html', args)



@login_required(login_url='/home/')
def viewMessage(request):
    """ Function to view the individual message you wish to see

    :param request: the HTTP request handled by Django
    :param message_id: the identification number of the message that's clicked on
    :return: a render_to_response call for the view_message.html page and the passed args
            args contains the mess = message to be viewed with a True is_read boolean
                              activeuser = the current logged in user
    """
    return