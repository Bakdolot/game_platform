from django.db.models.query_utils import select_related_descend
from rest_framework import serializers
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
        fields = ('title', 'create_at', 'description', 'game', 'status', 'start_date', 'rate', 'get_views_count', 'get_reposts_count', 'get_game_border')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'username')


class User2Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'user', 'whatsapp_phone', 'telegram_phone', 'get_likes', 'get_dislikes')


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


class CategoryBattlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ('get_game_icon', 'title', 'status', 'start_date', 'rate', 'get_views_count', 'get_reposts_count')