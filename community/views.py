from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .models import Community
from .forms import joinCommunityForm
from users.models import BaseUser
from tools.models import Tool

# Create your views here.
###
### __author__ = Shalimar
### User is shown a page with all the information about their community.
### -Statistics
### -Members (admins see pending as well)
### -Options to join/register different oommunity,
### -Admins should be able to accept, reject, promote, and remove users.
@login_required(login_url='/home/')
def viewCommunity(request, arg = None):
    if arg is None:
        args = {}
    else:
        args = arg
    args['in_default'] = False
    if request.user.community.id == 0:
        args['in_default'] = True
    args['community_members'] = BaseUser.objects.filter(community=request.user.community, pending=False)
    args['pending_community_members'] = BaseUser.objects.filter(community=request.user.community, pending=True)
    args['admins'] = BaseUser.objects.filter(community=request.user.community, is_admin=True)
    args['user_community'] = Community.objects.get(id=request.user.community.id)
    args['activeuser'] = request.user
    # TODO: pass in statistics as well.
    return render_to_response('community/community.html', args)


###
### __author__ = Shalimar
### User submits a form which creates a new community and adds the user into
### it as an admin.
### FRONT-END: If user is currently the only admin of their current community,
### they are required to appoint a new admin in their place before they can leave,
### unless they are the only person in the group.
###
@login_required(login_url='/home/')
def registerCommunity(request):
    if request.user.is_active:
        args = {}
        args['activeuser'] = request.user
        num_of_admins = len(BaseUser.objects.filter())
        if request.user.is_admin and num_of_admins == 1:
            args['message'] = {'error': 'In order to join a new community, please promote another admin in your place.'}
        # TODO: also check to make sure they are not currently set to borrow or lend any tools in the future.
        # If they are ask them to cancel reservations.
        elif request.method == 'POST':
            form = joinCommunityForm(request.POST)
            if form.is_valid():
                request.user.community = Community.objects.create(name=form.cleaned_data.get('community'))
                request.user.pending = False
                request.user.is_admin = True
                request.user.save()
                return HttpResponseRedirect('/community/')
            else:
                args['form']=joinCommunityForm()
        elif request.method == 'GET':
            args['form']=joinCommunityForm()
        return render_to_response('community/register_community.html', args)

###
### __author__ = Shalimar
### User is presented with all communities that exist, and upon choosing one is
### added to that community, unless the user is already part of that community.
### If the community is empty when the user joins, they become the admin of it.
### If it is not empty they join the waiting list for admins of the community
### to accept them.
### FRONT-END: If an admin attempts to change communities and is the only admin of the group
### he must appoint a new admin in his place, unless he is the only person in the community.
###
@login_required(login_url='/home/')
def joinCommunity(request):
    if request.user.is_active:
        args = {}
        args['activeuser'] = request.user
        args['communities'] = Community.objects.exclude(pk=0)
        num_of_admins = len(BaseUser.objects.filter())
        if request.user.is_admin and num_of_admins == 1:
            args['message'] = {'error': 'In order to join a new community, please promote another admin in your place.'}
        # TODO: also check to make sure they are not currently set to borrow or lend any tools in the future.
        # If they are ask them to cancel reservations.
        elif request.method == 'POST':
            form = joinCommunityForm(request.POST)
            if form.is_valid():
                new_community = Community.objects.get(name=form.cleaned_data.get('community'))

                # User can not join the same community, change nothing.
                if request.user.community == new_community:
                    return HttpResponseRedirect('/community/')

                # If new community is not the one user is currently in, update.
                request.user.community = new_community
                if BaseUser.objects.filter(community=new_community).count() > 0:
                    request.user.pending = True
                    request.user.is_admin = False
                else:
                    request.user.pending = False
                    request.user.is_admin = True
                request.user.save()
                args['message'] = {'success': 'Successfully joined new community'}
                return viewCommunity(request, args)
                #return HttpResponseRedirect('/community/')
            else:
                args['form'] = form
        elif request.method == 'GET':
            args['form'] = joinCommunityForm()
        return render_to_response('community/join_community.html', args)

###
### __author__ = Shalimar
### Admin accepts a user into the community and user's tools become delisted.
###
@login_required(login_url='/home/')
def acceptUser(request, user_id):
    args = {}
    user_to_accept = BaseUser.objects.get(user_id)
    if request.user.is_admin and request.user.community == user_to_accept.community:
        users_tools = Tool.objects.filter(owner=user_id)
        for tool in users_tools:
            tool.available = False
        user_to_accept.pending = False
        args['message'] = {'success': user_to_accept + ' has been accepted into your community.'}
    else:
        args['message'] = {'error': 'You do not have permission to accept ' + user_to_accept + ' into the community.'}
    return HttpResponseRedirect('/community/')
###
### __author__ = Shalimar
### Admin denies user entrance into the community and user is placed into the
### default community again, and must try joining another.
###
@login_required(login_url='/home/')
def denyUser(request, user_id):
    args = {}
    user_to_reject = BaseUser.objects.get(user_id)
    if request.user.is_admin and request.user.community == user_to_reject.community:
        user_to_reject.community = Community.objects.get(0)
        user_to_reject.pending = False
        args['message'] = {'success': user_to_reject + ' has been denied from joining your community.'}
    else:
        args['message'] = {'error': 'You do not have permission to deny ' + user_to_reject + ' from the community.'}
    return HttpResponseRedirect('/community/')

###
### __author__ = Shalimar
### Admin removes user from their community, they are placed in the default community.
###
@login_required(login_url='/home/')
def removeUser(request, user_id):
    args={}
    user_to_remove = BaseUser.objects.get(user_id)
    if request.user.is_admin and request.user.community == user_to_remove.community:
        user_to_remove.community = Community.objects.get(0)
        user_to_remove.pending = False
        args['message'] = {'success': user_to_remove + ' was removed successfully.'}
    else:
        args['message'] = {'error': 'You do not have permission to remove ' + user_to_remove + '.'}
    return HttpResponseRedirect('/community/')

###
### __author__ = Shalimar
### Admin promotes another user to admin status.
###
@login_required(login_url='/home/')
def promoteUser(request, user_id):
    args = {}
    user_to_promote = BaseUser.objects.get(user_id)
    if request.user.is_admin and request.user.community == user_to_promote.community:
        user_to_promote.is_admin = True
        args['message'] = {'success': user_to_promote + ' was promoted successfully and is now an admin.'}
    else:
        args['message'] = {'error': 'You do not have permission to promote ' + user_to_promote + '.'}
    return HttpResponseRedirect('/community/')