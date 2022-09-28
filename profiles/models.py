# The code is based on  "Adam Lapinski's" walk-through project "Moments"!
# https://github.com/Code-Institute-Solutions/moments

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    # 1:1 field pointing to user instances, if deleted, all data connected to it
    # will be deleted as well (cascade)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    # when (date) was created
    created_at = models.DateTimeField(auto_now_add=True)
    # when (date) was updated
    updated_at = models.DateTimeField(auto_now=True)
    # is optional (blank=True), name of the user
    name = models.CharField(max_length=255, blank=True)
    # is optional (blank=True), text about the user
    content = models.TextField(blank=True)
    # user profile picture, uses a default picture from cloudinary
    image = models.ImageField(
        upload_to='images/', default='../default_profile_ukustm'
    )

    # sorts the user profiles in the admin starting with the newest profile
    class Meta:
        ordering = ['-created_at']

    # returns information about who the owner of the profile is in the admin panel
    def __str__(self):
        return f"{self.owner}'s profile"

def create_profile(sender, instance, created, **kwargs):
    """
    if created (is a Boolean value, true if instance was created) is true,
    create profile who's owner is that user who created that instance
    """
    if created:
        Profile.objects.create(owner=instance)

# every time a user is created (sign-up/ sender=User) a signal is send which runs
# the function "create_profile" which will create a user profile
post_save.connect(create_profile, sender=User)