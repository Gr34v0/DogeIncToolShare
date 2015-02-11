from django.db import models
from users.models import *


# Create your models here.

class Tool(models.Model):
    """ Tool objects to be saved into the database as viewable, searchable tools

    """
    owner = models.ForeignKey(BaseUser)
    tool_type = models.CharField(('tool_type'), max_length=40, blank=True)
    description = models.CharField(('description'), max_length=100, blank=True)
    available = models.BooleanField()
    curr_holder = models.IntegerField()
    pending = models.BooleanField()
    
    def __str__(self):
        return self.tool_type + ": " + self.owner.username
    def setOwner(self, owner):
        """ setting the owner of the tool upon creation of the object

        :param owner: entire BaseUser object, generally the activeuser
        :return: n/a
        """
        self.owner = owner
    def setAvailable(self, available):
        """ setting the availability of the tool either upon creation, upon borrowing or upon returning of the tool

        :param available: Boolean that a user chooses and passes to the function
        :return: n/a
        """
        self.available = available
    
    #REQUIRED_FIELDS = ['tool_type', 'description',]
        
class ToolRequest(models.Model):
    """ ToolRequest objects to be saved into the database as a request

    """
    sender = models.ForeignKey(BaseUser, related_name = "request_sender")
    receiver = models.ForeignKey(BaseUser, related_name = "request_receiver")
    tool = models.OneToOneField(Tool)
    duration = models.IntegerField()
    accepted = models.BooleanField()
