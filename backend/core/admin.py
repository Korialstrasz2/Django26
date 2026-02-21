from django.contrib import admin
from core.models import PlayerProfile, UserSettings


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_master')
    search_fields = ('user__username',)
    list_filter = ('is_master',)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'selected_style_folder')
    search_fields = ('user__username', 'selected_style_folder')
