from django.contrib.auth.models import User
from django.db import models


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player_profile')
    is_master = models.BooleanField(default=False)

    def __str__(self) -> str:
        role = 'master' if self.is_master else 'player'
        return f'{self.user.username} ({role})'


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    selected_style_folder = models.CharField(max_length=120, blank=True, default='')

    def __str__(self) -> str:
        selected = self.selected_style_folder or 'none'
        return f'{self.user.username} settings ({selected})'
