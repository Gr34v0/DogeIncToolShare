from .models import *
from django import forms
from django.http import *
import sys
sys.path.append("/DogeIncToolShare")
from users.models import *
from tools.models import *

class ToolForm(forms.ModelForm):
    """ Form for registering tools with the Tool objects

    """
    tool_type = forms.CharField(max_length=40, label="Tool Type: ")
    description = forms.CharField(max_length=100, label="Description: ")
    available = forms.BooleanField(required = False)
    owner = forms.ModelChoiceField(queryset = BaseUser.objects.all(),
                                  	widget=forms.HiddenInput())
    curr_holder = forms.IntegerField(required = False, widget = forms.HiddenInput())
    class Meta:
        model = Tool

class NavSearchForm(forms.Form):
    """ Form for use as a search bar for tools

    """
    search = forms.CharField(max_length=30, required=False)

class ToolRequestForm(forms.ModelForm):
    """ Form for requesting a tool; to be used with the ToolRequest objects

    """
    sender = forms.ModelChoiceField(queryset = BaseUser.objects.all(),
                                  	widget=forms.HiddenInput(), required = False)
    receiver = forms.ModelChoiceField(queryset = BaseUser.objects.all(),
                                  	widget=forms.HiddenInput(), required = False)
    tool = forms.ModelChoiceField(queryset = Tool.objects.all(),
                                  	widget=forms.HiddenInput(), required = False)
    duration = forms.IntegerField(required = True )
    accepted = forms.BooleanField(widget=forms.HiddenInput(), required = False)

    class Meta:
        model = ToolRequest
