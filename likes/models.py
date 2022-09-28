# The code is based on  "Adam Lapinski's" walk-through project "Moments"!
# https://github.com/Code-Institute-Solutions/moments

from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe


class Like(models.Model):
    """
    Like model, related to 'owner' and 'recipe'.
    'owner' is a User instance and 'recipe' is a Recipe instance.
    'unique_together' makes sure a user can't like the same recipe twice.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, related_name='likes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'recipe']

    def __str__(self):
        return f'{self.owner} {self.recipe}'