from django.contrib import admin

from .models import *


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'username', 'is_active']
    list_display_links = list_display
    inlines = (UserProfileInline,)


admin.site.register(User, UserAdmin)
admin.site.register(Identification)
admin.site.register(BattleHistory)
admin.site.register(UserScores)
admin.site.register(Notification)
admin.site.register(UserComment)
