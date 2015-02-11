from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from .forms import *
from users.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

from django.http import *
from .models import Tool
from itertools import chain

##def tool_register_auth(request):
##    pass
####    username = request.POST.get('username', '')
####    password = request.POST.get('password', '')
####    user = auth.authenticate(username=username, password=password)
####
####    if user is not None:
####        return HttpResponseRedirect('/tools/tool_register/')
####    else:
####        return HttpResponseRedirect('/user_register/invalid')

@login_required
def tool_register(request):
    """ Function to call the tool_register.html

    :param request: HTTP request object handled by Django
    :return: a call to the display_tools function which is passed a request and args if method is POST
            or a render_to_response call for the tool_register.html page and args if method is anything else (GET)

            args contains an activeuser, and either a success message, error message or a ToolForm
    """
    args = {}
    args['activeuser'] = request.user
    if request.method == 'POST':
        frm = ToolForm(request.POST)
        if frm.is_valid():
            new_tool = Tool.objects.create(
                            tool_type=frm.cleaned_data['tool_type'],
                            description=frm.cleaned_data['description'],
                            available=frm.cleaned_data['available'],
                            owner=frm.cleaned_data['owner'],
                            curr_holder=request.user.id,
                            pending = False)
            new_tool.save()
            args['message'] = {'success': 'Tool successfully register'}
            # args['tools'] = Tool.objects.filter(owner_id = request.user.id)
            # args['borrowed_tools'] = Tool.objects.filter(curr_holder = request.user.id)
            # args['borrowed_tools'] = args['borrowed_tools'].exclude(owner = request.user.id)
            # return render(request, 'tools/display_tools.html', args)
            return display_tools(request, args)
        else:
            args['message'] = {'error': 'Error registering tool'}
    else:
        frm = ToolForm(initial = {'owner':request.user, 'curr_holder':request.user.id})

    #args.update(csrf(request))

    args['form'] = frm
    return render_to_response('tools/tool_register.html', args)

@login_required
def tool_management(request):
    """

    :param request:
    :return:
    """
    return HttpResponse("You are at the tool management page")

@login_required
def tool_edit(request, tool_id):
    """ Function to call the tool editing page

    :param request: HTTP request handled by Django
    :param tool_id: the id of the tool the user is editing
    :return: a HttpResponseRedirect to display_tools.html if the current user and the tool's owner do not match,
            a render_to_response call for tool_edit.html with args containing the updated form, the current tool and
                the active user if the method is POST and either a success or error message,
            or a 404 HttpResponseRedirect.
    """
    args = {}
    try:
        curr_tool = Tool.objects.get(pk = tool_id)
        if curr_tool.owner != request.user:
            return HttpResponseRedirect("../../../tools/display_tools")
        if request.method == 'POST':
            frm = ToolForm(request.POST, instance = curr_tool)
            if frm.is_valid():

                j = frm.save(commit = False)
                j.save()
                # args['activeuser'] = request.user
                args['message'] = {'success': 'Tool edit successful'}
                # args['tools'] = Tool.objects.filter(owner_id = request.user.id)
                # args['borrowed_tools'] = Tool.objects.filter(curr_holder = request.user.id)
                # args['borrowed_tools'] = args['borrowed_tools'].exclude(owner = request.user.id)
                # return render_to_response('tools/display_tools.html', args)
                return view_tool(request, tool_id, args)
            else:
                args['message'] = {'error': 'Error editing tool'}
        else:
            frm = ToolForm(instance = curr_tool)

        #args.update(csrf(request))

        args['form'] = frm
        args['tool'] = curr_tool
        if request.user.is_active:
            args['activeuser'] = request.user

        return render_to_response('tools/tool_edit.html', args)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("../../404.html")

@login_required
def view_tool(request, tool_id, args = None):
    """ Function to view a single specific tool

    :param request: HTTP request handled by Django
    :param tool_id: ID of tool to be viewed
    :param args: None-type variable
    :return: render_to_response call for view_tool.html with args containing the activeuser, the tool and the tool's holder
            or HttpResponseRedirect to browse_tools if the tool is outside the active user's community
            or a 404 HttpResponseRedirect
    """
    try:
        if args is None:
            args = {}

        curr_tool = Tool.objects.get(pk = tool_id)
        if curr_tool.owner.zipcode != request.user.zipcode:
            return HttpResponseRedirect('../../tools/browse_tools/')
        args['tool'] = curr_tool
        if request.user.is_active:
            args['activeuser'] = request.user
            args['curr_holder'] = BaseUser.objects.get(pk = request.user.id)
        return render_to_response('tools/view_tool.html', args)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("../../404.html")

@login_required
def borrow_tool(request, tool_id):
    """ Function to borrow a tool

    :param request: HTTP request handled by Django
    :param tool_id: ID of the tool to be borrowed
    :return: HttpResponseRedirect call to browse_tools.html
    """
    if request.user.is_active:
        curr_tool = Tool.objects.get(pk = tool_id)
        if curr_tool.available and request.user.id != curr_tool.owner.id:
            #return HttpResponseRedirect("borrow/" + str(tool_id) + "/" + str(curr_tool.owner.id) + "/")
           # return HttpResponseRedirect(str(curr_tool.owner.id) + "/", request)
           curr_tool.curr_holder = request.user.id
           curr_tool.available = False
           curr_tool.save()
        args = {}
        args['curr_tool'] = curr_tool
        args['activeuser'] = request.user
        # return render_to_response('tools/borrow_success.html', args)
        return HttpResponseRedirect("../../browse_tools")

@login_required
def send_tool_request(request, tool_id, receiver_id):
    """ Function for sending a tool borrow request

    :param request: HTTP request handled by Django
    :param tool_id: ID of the tool being requested
    :param receiver_id: ID of the person receiving the request
    :return: HttpResponseRedirect to browse_tools.html if method is POST
            or a render_to_response call to tool_request.html with args containing a ToolRequestForm, activeuser and
                the IDs for the tool and user receiving the request if the method is anything else (GET)
    """
    if request.method == 'POST':
        frm = ToolRequestForm(request.POST)
        if frm.is_valid():
            curr_tool = Tool.objects.get(pk = tool_id)
            curr_tool.pending = True
            receiver_user = BaseUser.objects.get(pk = receiver_id)
            new_tool_request = ToolRequest.objects.create(
                            sender = request.user,
                            receiver = receiver_user, 
                            tool = curr_tool, 
                            duration=frm.cleaned_data['duration'], 
                            accepted=False)
            new_tool_request.save()
            return HttpResponseRedirect("../../browse_tools")
    else:
        frm = ToolRequestForm()

    args = {}
    #args.update(csrf(request))

    args['form'] = frm
    args['activeuser'] = request.user
    args['tool_id'] = tool_id
    args['receiver_id'] = receiver_id

    return render_to_response('tools/tool_request.html', args)

"""
Note this should not go to success page
"""
@login_required
def edit_tool_request(request, tool_request_id):
    """ Function to call an edit to an out-standing tool request

    :param request: HTTP request handled by Django
    :param tool_request_id: ID of the tool request object in question
    :return: render_to_response call for edit_success.html if method is POST
            or render_to_response call for tool_edit.html with args containing a ToolRequstForm filled with the current object data,
                the tool request object itself and the activeuser if method is not POST (GET)
    """
    curr_tool_request = ToolRequest.objects.get(pk = tool_request_id)
    if request.method == 'POST':
        frm = ToolRequestForm(request.POST, instance = curr_tool_request)
        if frm.is_valid():
            j = frm.save(commit = False)
            j.save()
            return render_to_response('tools/edit_success.html')
    else:
        frm = ToolRequestForm(instance = curr_tool_request)

    args = {}
    #args.update(csrf(request))

    args['form'] = frm
    args['tool_request'] = curr_tool_request
    if request.user.is_active:
        args['activeuser'] = request.user

    return render_to_response('tools/tool_edit.html', args)


@login_required
def return_tool(request, tool_id):
    """ Function to "return" a borrowed tool to it's original owner

    :param request: HTTP request handled by Django
    :param tool_id: ID of the tool
    :return: HttpResponseRedirect to browse_tools.html
    """
    if request.user.is_active:
        curr_tool = Tool.objects.get(pk = tool_id)
        if request.user.id == curr_tool.curr_holder or request.user == curr_tool.owner:
            curr_tool.available = True
            curr_tool.curr_holder = curr_tool.owner.id
            curr_tool.save()
        args = {}
        args['curr_tool'] = curr_tool
        args['activeuser'] = request.user
        return HttpResponseRedirect("../../browse_tools")

def display_tools(request, args = None):
    """ Function to display tools available for the user to borrow.

    :param request: HTTP request handled by Django
    :param args: None-Type variable
    :return: render_to_response call for display_tools.html and args containing tools (all tools owned by the user),
                borrowed tools (all tools currently held by the user that aren't owned by them) and the activeuser.
    """
    if args is None:
        args = {}

    #args.update(csrf(request))

    args['tools'] = Tool.objects.filter(owner_id = request.user.id)
    args['borrowed_tools'] = Tool.objects.filter(curr_holder = request.user.id)
    args['borrowed_tools'] = args['borrowed_tools'].exclude(owner = request.user.id)
    if request.user.is_active:
        args['activeuser'] = request.user

    return render_to_response('tools/display_tools.html', args)

def browse_tools(request, args = None):
    """ Function for browsing the tools in the community the user can borrow

    :param request: HTTP request handled by Django
    :param args: None-type variable
    :return: render_to_response call for browse_tools.html and args containing tools
                (avaliable tools that share the commuinty the user is in) and activeuser
    """
    if args is None:
        args = {}

##    comm = BaseUser.objects.filter(zipcode = request.user.zipcode)
    tools = Tool.objects.filter(owner = BaseUser.objects.filter(community = request.user.community), available = True)
    tools = tools.exclude(owner = request.user)
##    for user in comm:
##        tools = (chain(Tool.objects.filter(owner = user), tools))
    args['tools'] = tools
    if request.user.is_active:
        args['activeuser'] = request.user
    return render_to_response('tools/browse_tools.html', args)

#for some reason will only return tools that do not belong to you
#it's a feature not a bug ;)
def search(request):
    """ Function for searching for a tool that matches a specific string

    :param request: HTTP request handled by Django
    :return: render_to_response for search.html and args containing the results (tools that match the
                search query held in the request), and activeuser
    """
    args = {}
    query = request.GET.get('query')

    if query:
        #This filter ignores the case and allows substrings
        tools = Tool.objects.filter(tool_type__icontains = query, owner = BaseUser.objects.filter(community = request.user.community))
        if len(tools) > 0:
            args['results'] = tools.exclude(owner = request.user)
        else:
            tools = Tool.objects.filter(owner = BaseUser.objects.filter(community = request.user.community), available = True)
            args['results'] = tools.exclude(owner = request.user)
    else:
        tools = Tool.objects.filter(owner = BaseUser.objects.filter(community = request.user.community), available = True)
        args['results'] = tools.exclude(owner = request.user)

    if request.user.is_active:
        args['activeuser'] = request.user
    return render_to_response('tools/search.html', args)

##def delete_tool(request, tool_id):
##    Tool.objects(pk = tool_id).delete()
# def display_tool(request, tool_id=1):
#     return render(request, 'display_tool.html',
#                   {'tool': tools.objects.get(id=tool_id) })
