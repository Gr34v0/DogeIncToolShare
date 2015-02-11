__author__ = 'Christian'

from django.contrib.auth.models import AbstractUser, models, validators
from community.models import Community

# Create your models here.


class BaseUser(AbstractUser):
    """ Class that is the framework for all users that register into the system.

    Replaces Django's built in users because there was some functionality we needed
    that Django didn't provide and some functionality Django did provide that we didn't need.
    """

    zipcode = models.CharField(('Zipcode'), max_length=5, blank=True,
    help_text=('Required. Must be 5 digits long'),

    validators=[
        validators.RegexValidator(r'^[0-9]{5}$',
                                     ('Enter a valid zipcode.'
                                      'This value may contain only numbers'),
                                      'invalid'),
    ],
    error_messages={
        'invalid': ("Zipcode is of invalid length."),
    })

    address = models.CharField(('Address'), max_length=40, blank=True)

    community = models.ForeignKey(Community, default=0) #ForeignKey to reference the community the user is in with the database

    pending = models.BooleanField(default=False) #is True when user is waiting for confirmation to enter a community
    is_admin = models.BooleanField(default=False) #is True when user creates their own community

    class Meta:
        verbose_name = 'Base User'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name',
                       'last_name',
                       'zipcode',
                       'address',
    ]

    def getModelData(self):
        return self._meta.fields