__author__ = 'Christian'

from users.models import BaseUser
from django import forms

class UserForm(forms.ModelForm):
    """ Form class that extends the Django ModelForm to be used with the BaseUser class from users/models.py to create a
    new BaseUser object to be saved into the database

    """
    required_css_class = 'required'

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label="Username",
                                error_messages={'invalid': "Value must be alphanumerics and/or @/./+/-/_ characters."})

    first_name = forms.CharField(max_length=30,
                                 label="First name",
                                 error_messages={'invalid': "You must have a first name."})

    last_name = forms.CharField(max_length=30,
                                label="Last name",
                                error_messages={'invalid': "You must have a last name."})

    email = forms.EmailField(label="E-mail")

    address = forms.CharField(max_length=40,
                              label="Address",
                              error_messages={'invalid': "Value must be an address for your tool pickup location."})

    age_eligible = forms.BooleanField(required=True)

    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password (again)")

    class Meta:
        model = BaseUser
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'password1', 'password2']

    def save(self, commit=True):
        """ Modified default Django save() function from the default forms to account for our new UserForm class

        :param commit: Boolean to indicate to save the new user to the database
        :return: new BaseUser object generated from the UserForm fields
        """
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean_username(self):
        """ Checks to see if the string in the UserForm username field is unique to the database

        :return: the verified unique username, assuming the not-unique error isn't raised
        """
        existing = BaseUser.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.") #not-unique error
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """ Checks to see if the string in the UserForm email field is unique to the database

        :return: the verified unique, assuming the not-unique error isn't raised
        """
        #if you want unique email address. else delete this function
        if BaseUser.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.") #not-unique error
        return self.cleaned_data['email']

    def clean(self):
        """ Checks the password fields of the UserForm to see if they contain different information

        :return: the entire cleaned_data form, assuming the password-mismatch error isn't raised
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields didn't match.") #password-mismatch error
        return self.cleaned_data




class UserUpdateForm(forms.ModelForm):
    """ Modified version of UserForm specifically for updating non-critical account information

    """

    first_name = forms.CharField(max_length=30,
                                 label="First name",
                                 error_messages={'invalid': "You must have a first name."})

    last_name = forms.CharField(max_length=30,
                                 label="Last name",
                                 error_messages={'invalid': "You must have a last name."})

    email = forms.EmailField( label="E-mail",
                              error_messages={'unique':'Email address is already registered.'})

    address = forms.CharField(max_length=40,
                              label="Address",
                              error_messages={'invalid': "Value must be an address for your tool pickup location."})

    class Meta:
        model = BaseUser
        fields = ['first_name', 'last_name', 'email', 'address']

    def save(self, commit=True):
        """ Modified UserForm save() function to remove password-related operations and change the form used

        :param commit: Boolean to indicate to save the new user to the database
        :return: new BaseUser object generated from the UserForm fields
        """
        user = super(UserUpdateForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserSecurityForm(forms.ModelForm):
    """ Modified version of UserForm specifically for updating critical account information

    """

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label="Username",
                                error_messages={'invalid': "Value must be alphanumerics and/or @/./+/-/_ characters."})

    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password (again)")

    class Meta:
        model = BaseUser
        fields = ['password1', 'password2', 'username']

    def clean(self):
        """ Checks the password fields of the UserSecurityForm to see if they contain different information

        :return: the entire cleaned_data form, assuming the password-mismatch error isn't raised
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data

    def save(self, commit=True):
        """ Modified UserForm save() function to change the form used

        :param commit: Boolean to indicate to save the new user to the database
        :return: new BaseUser object generated from the UserForm fields
        """
        user = super(UserSecurityForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user