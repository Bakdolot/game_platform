from os import set_inheritable
from django.db.models import fields
from django.db.models.fields import files
from django.db.models.query_utils import select_related_descend
from django.views import generic
from rest_framework import generics, serializers
from .models import *
from django.conf import settings
from accounts.models import UserProfile, User


class BattleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ('title', 'status', 'start_date', 'rate', 'get_views_count', 'get_reposts_count', 'get_game_icon')


class BattleMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleMembers
        fields = '__all__'


class DetailBattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ('title', 'create_at', 'description', 'game', 'winner', 'status', 'start_date', 'rate', 'get_views_count', 'get_reposts_count', 'get_game_border')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'username')


class User2Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'user', 'whatsapp_phone', 'telegram_phone', 'get_likes_count', 'get_dislikes_count')


class BattleUserSerializer(serializers.Serializer):
    user=UserSerializer()
    user2 = User2Serializer()


class SimilarBattlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ('get_game_icon', 'title', 'rate')


class AllBattlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('get_game_border', 'name', 'get_battles', 'get_followers', 'get_category_name')


class GameBattlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ('get_game_icon', 'title', 'status', 'start_date', 'rate', 'get_views_count', 'get_reposts_count')



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CreateBattleMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleMembers
        fields = '__all__'


class CreateBattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        exclude = ['views', 'reposts', 'create_at', 'status']


class BattleEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ('title', 'description', 'start_date', 'owner', 'status', 'rate')


class BattleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleResponse
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'


class QuestionHelpSerializer(serializers.ModelSerializer):
    class Metal:
        model = QuestionHelp
        fields = '__all__'


class MainBattleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleResponse
        fields = '__all__'