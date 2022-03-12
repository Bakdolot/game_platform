from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.contrib.auth.password_validation import validate_password
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.fields import CurrentUserDefault

from .models import (
    Identification, 
    Notification, 
    User, 
    UserComment, 
    UserProfile, 
    UserScores,
    BattleHistory
)
from main.models import Game, Battle
from .choices import SendCodeType
from .utils import SendSMS, get_otp
from .validators import phone_validator

from uuid import uuid4


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
        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    

class UserSendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phone_validator], required=True)
    type = serializers.ChoiceField(choices=SendCodeType.choices, required=True)

    def validate(self, attrs):
        if attrs['type'] == SendCodeType.RESET_PHONE:
            return attrs
        try:
            self.instance = User.objects.get(phone=attrs['phone'])
            return attrs
        except User.DoesNotExist as err:
            raise ValidationError(err)
    
    def send_otp_code(self):
        data = self.validated_data
        phone = data['phone']
        code = get_otp()
        cache.set(code, phone, settings.SMS_CODE_TIME, version=data['type'])
        SendSMS(phone, code).send


class RegisterCodeVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)

    def validate(self, attrs):
        phone = cache.get(attrs['code'], version=SendCodeType.REGISTER)
        if phone is not None:
            self.instance = User.objects.get(phone=phone)
            return attrs
        raise ValidationError(_('не правельный код'))
    
    def update(self):
        self.instance.is_active = True
        self.instance.save()
        return self.instance


class PasswordResetVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)

    def validate_password(self, password):
        try:
            validate_password(password)
            return password
        except ValidationError as exc:
            raise ValidationError(exc)

    def validate_code(self, code):
        phone = cache.get(code, version=SendCodeType.RESET_PASSWORD)
        if phone is not None:
            self.instance = User.objects.get(phone=phone)
            return code
        raise ValidationError(_('не правельный код'))
    
    def update(self):
        self.instance.set_password(self.validated_data['password'])
        self.instance.save()
        return self.instance


class PhoneResetVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)

    def validate(self, attrs):
        phone = cache.get(attrs['code'], version=SendCodeType.RESET_PHONE)
        if phone is not None:
            attrs['new_phone'] = phone
            return attrs
        raise ValidationError(_('не правельный код'))
    
    def update(self, instance):
        instance.phone = self.validated_data['new_phone']
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    battles = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'image', 'balance', 
            'whatsapp_phone', 'telegram_phone', 'description', 'steem_account', 
            'likes_count', 'dislikes_count', 'battles', 'rate']

    def get_likes_count(self, instance):
        return instance.likes.all().count()
    
    def get_dislikes_count(self, instance):
        return instance.dislikes.all().count()

    def get_battles(self, instance):
        return {
            'battles': BattleHistory.objects.filter(user = instance.user).count(),
            'victories': BattleHistory.objects.filter(user = instance.user, result='2').count(),
            'defeats': BattleHistory.objects.filter(user = instance.user, result='1').count(),
        }
    
    def get_rate(self, instance):
        courtesy = 0
        user_scores = UserScores.objects.filter(user__id=instance.id)
        if instance.courtesy_rate_sum:
            courtesy = instance.courtesy_rate_sum / user_scores.filter(type='1').count()
        punctuality = 0
        if instance.punctuality_rate_sum:
            punctuality = instance.punctuality_rate_sum / user_scores.filter(type='2').count()
        adequacy = 0
        if instance.adequacy_rate_sum:
            adequacy = instance.adequacy_rate_sum / user_scores.filter(type='3').count()
        return {
            'courtesy': courtesy,
            'punctuality': punctuality,
            'adequacy': adequacy
        }


class UserBattlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ['title', 'rate', 'start_date', 'status', 'get_game_icon']


class CreateScoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScores
        fields = '__all__'
        

class UserGameResultsSerializer(serializers.ModelSerializer):
    battles = serializers.SerializerMethodField()
    victories = serializers.SerializerMethodField()
    defeats = serializers.SerializerMethodField()
    victory_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = ['name', 'icon', 'battles', 'victories', 'defeats', 'victory_percent']
    
    def get_battles(self, instance):
        self.user_battles = BattleHistory.objects.filter(battle__game=instance, user=CurrentUserDefault)
        return self.user_battles.count()
    
    def get_victories(self, instance):
        return self.user_battles.filter(result='2').count()

    def get_defeats(self, instance):
        return self.user_battles.filter(result='1').count()

    def get_victory_percent(self, instance):
        victory_percent = 0
        battle_count = self.user_battles.count()
        victories = self.user_battles.filter(result='2').count()
        if battle_count:
            victory_percent = (victories * 100) / battle_count
        return victory_percent
    

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = '__all__'


class UserIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = '__all__'


class AllUsersSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'image']
    
    def get_username(self, instance):
        return instance.user.username


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = [
            'user',
            'likes', 
            'dislikes', 
            'balance', 
            'courtesy_rate_sum',
            'punctuality_rate_sum',
            'adequacy_rate_sum'
            ]


class UserCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = ['owner', 'text', 'create_at']
