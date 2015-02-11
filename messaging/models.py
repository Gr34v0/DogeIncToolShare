from django.db import models
from users.models import BaseUser

# Create your models here.



class Message(models.Model):
    """ Class that is the framework for all messages that get registered into the database

    """

    from_user = models.ForeignKey(BaseUser, null=True, related_name='creator')
    to_user = models.ForeignKey(BaseUser, null=True, related_name='receiver')
    subject_line = models.CharField(('Subject'), max_length=140, blank=True,)

    is_read = models.BooleanField(('Read'), default=False)

    body_text = models.CharField(('Body'), max_length=1000, blank=True,)

    def setAsRead(self):
        """ Flips the is_read boolean to determine if the message has been seen/read yet

        :return: n/a
        """
        self.is_read = True