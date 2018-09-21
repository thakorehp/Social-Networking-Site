from django.db import models
from django.contrib.auth.models import User
from django import forms
from thanos import settings
from datetime import datetime
import json
from django.utils.six import python_2_unicode_compatible
from channels import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .settings import MSG_TYPE_MESSAGE
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	user_profile = models.ImageField(blank=True)
	Birthdate = models.DateField(blank=True)
	about = models.CharField(max_length=2000,blank=True)

	def age(self):
		import datetime
		return int((datetime.date.today() - self.Birthdate).days / 365.25)

def gettime():
    return datetime.now().time()

def getdate():
    return datetime.now().date()
    
class Post(models.Model):
    user = models.ForeignKey(User)
    fetch = models.BooleanField(default=False)
    post_img = models.ImageField(blank=True)
    post_msg = models.CharField(max_length=1000,blank=True)
    post_date = models.DateField(default=getdate())
    post_time = models.TimeField(default=gettime())   


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)


@python_2_unicode_compatible
class Room(models.Model):
    """
    A room for people to chat in.
    """
    id = models.IntegerField(primary_key=True,unique=True)
    # Room title
    title = models.CharField(max_length=255)
    
    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )

    


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.IntegerField()
    User = models.TextField()
    sender = models.TextField()
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    fetch = models.BooleanField(default=True)


    def add_notification(self,rid,rec,sen):
            notification = Notification(room_id=rid,User=rec, sender = sen,message="You have a Chat Invitation",fetch=False)
            notification.save()