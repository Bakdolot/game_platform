from django.urls import path
from django.utils.module_loading import autodiscover_modules
from .views import *


urlpatterns = [
    path('battles/', BattleListView.as_view()),
    path('battle/detail/<int:id>/', BattleDetailView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('category/detail/<int:id>/', DetailCategoryView.as_view()),
    path('category2/detail/<int:id>/', DetailCategoryView2.as_view()),
]