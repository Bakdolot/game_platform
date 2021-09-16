from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.exceptions import (AuthenticationFailed, ValidationError)

from .models import Identification, Notification, User, UserComment, UserProfile, UserScores
from main.models import Game, Battle
from fcm_django.models import FCMDevice


class FcmCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'image', 'balance', 
            'whatsapp_phone', 'telegram_phone', 'description', 'steem_account', 
            'get_likes_count', 'get_dislikes_count', 'get_battles', 'get_rate']


class UserBattlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ['title', 'rate', 'start_date', 'status', 'get_game_icon']


class UserPlayedGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['name', 'icon']


class CreateScoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScores
        fields = '__all__'


class UserGameResultsSerializer(serializers.Serializer):
    game = UserPlayedGamesSerializer(many=True)
    battles = serializers.IntegerField()
    victories = serializers.IntegerField()
    defeats = serializers.IntegerField()
    victory_percent = serializers.IntegerField()


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = '__all__'


class UserIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['likes', 'dislikes']


class UserCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = ['owner', 'text', 'create_at']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['phone', 'username', 'password']
        extra_kwargs = {'write_only': True}

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return password

    def create(self, validated_data):
        _user = get_user_model()
        phone = validated_data.get('phone', '')
        username = validated_data.get('username', '')
        password = validated_data.get('password', '')
        user = _user.objects.create_user(phone=phone, username=username,
                                         password=password)
        user.is_active = False
        user.save()
        return user


class SetNewPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    code = serializers.CharField(max_length=4, required=True)
    password = serializers.CharField(write_only=True, min_length=1,
                                     required=True)
    password2 = serializers.CharField(write_only=True, min_length=1,
                                      required=True)

    class Meta:
        fields = ['phone', 'code', 'password', 'password2']

    def validate(self, attrs):
        try:
            phone = attrs.get('phone', '')
            password = attrs.get('password', '')
            password2 = attrs.get('password2', '')
            code = attrs.get('code', '')
            user = User.objects.get(phone=phone)
            if code != user.otp:
                raise AuthenticationFailed('Code is incorrect')
            if password == password2:
                user.set_password(password)
                user.save()
            elif password != password2:
                raise AuthenticationFailed('Password is not match')
        except User.DoesNotExist:
            raise AuthenticationFailed('User is not exists')
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password field didn\'t match.'})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
