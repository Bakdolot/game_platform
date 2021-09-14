from main.serializers import BattleMembersSerializer
from django.contrib import admin
from .models import *

admin.site.register(Battle)
admin.site.register(Category)
admin.site.register(Game)
admin.site.register(BattleMembers)
admin.site.register(BattleResponse)
admin.site.register(Questions)
admin.site.register(QuestionHelp)