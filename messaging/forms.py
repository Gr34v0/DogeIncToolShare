from .models import *
from django import forms
from django.http import *
import sys
sys.path.append("/DogeIncToolShare")
from users.models import *
from .models import *

class MessageForm(forms.ModelForm):
    """ Form that extends Django's ModelForm in order to create a new Message object that will be saved into the database

    """
    from_user = forms.ModelChoiceField(queryset=BaseUser.objects.all(), widget=forms.HiddenInput())

    to_user = forms.ModelChoiceField(queryset=BaseUser.objects.all(), widget=forms.HiddenInput())

    subject_line = forms.CharField(max_length=140)

    is_read = forms.BooleanField(required=False)

    body_text = forms.CharField(max_length=1000)

    class Meta:
        model = Message