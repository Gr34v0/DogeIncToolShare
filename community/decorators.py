__author__ = 'Christian'

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .models import Community
from .forms import joinCommunityForm
from users.models import BaseUser
from tools.models import Tool
from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.utils.six.moves.urllib.parse import urlparse
from django.shortcuts import resolve_url



def clean_user(request, func=None, login_url=None):
    if request.user.community.id == 0:
        return

    if request.user.pending == True:
        return

    return func(request)