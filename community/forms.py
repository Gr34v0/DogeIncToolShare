__author__ = 'Shalimar'

from django import forms
from .models import Community

class joinCommunityForm(forms.ModelForm):
    community = forms.CharField(required=True,
                                label="Communities",
                                max_length=100,
                                error_messages={'invalid': "You must join a community."})
    class Meta:
        model = Community
        fields = ['community']