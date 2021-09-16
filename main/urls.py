from django.urls import path
from django.utils.module_loading import autodiscover_modules
from .views import *


urlpatterns = [
    path('battles/', BattleListView.as_view()),
    path('battle/detail/<int:id>/', BattleDetailView.as_view()),
    path('games/', GameView.as_view()),
    path('game/detail/<int:id>/', DetailGameView.as_view()),
    path('game2/detail/<int:id>/', DetailGameView2.as_view()),
    path('follow_to_game/', FollowToGame.as_view()),
    path('categories/', CategoryView.as_view()),
    path('create_battle/', CreateBattleView.as_view()),
    path('create_battle_members/', CreateBattleMembersView.as_view()),
    path('question/', QuestionView.as_view()),
    path('battle_response/', MainBattleResponseView.as_view()),
]