from main.models import Game
from random import randint, choices
from string import ascii_letters
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from fcm_django.models import FCMDevice

from .utils import send_message_code, generate_code
from .models import *


class FcmCreateView(UpdateAPIView):
    serializer_class = FcmCreateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=request.data['user'])
        if user:
            try:
                fcm = FCMDevice.objects.get(user=request.data['user'])
                fcm.registration_id = request.data['registration_id']
                fcm.type = request.data['type']
                fcm.active = request.data['active']
                fcm.save()
            except FCMDevice.DoesNotExist:
                FCMDevice.objects.create(
                    user=user,
                    name=request.data['name'],
                    device_id=request.data['device_id'],
                    registration_id=request.data['registration_id'],
                    type=request.data['type'],
                )

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_queryset().user
        user_ser = self.get_serializer(self.get_queryset())
        user_score = UserScores.objects.get(user=user)
        user_score_ser = UserScoreSerializer(user_score)
        user_comments = UserComment.objects.filter(user__in=[user])
        user_comments_ser = UserComment(user_comments, many=True)
        games = []
        for game in Game.objects.filter(followers=user):
            battle = BattleHistory.objects.filter(battle__game=game, user=user)
            games.append({
                'game': game.name,
                'battles': battle.count(),
                'victories': battle(result='2').count(),
                'defeats': battle(result='1').count(),
                'victory_percent': (battle(result='2').count() * 100) / battle.count()
            })
        games_ser = UserGameResultsSerializer(games, many=True)
        return Response({
            'Profile': user_ser.data,
            'User score': user_score_ser.data,
            'Comments': user_comments_ser.data,
            'Games': games_ser.data
        })
        

class NotificationView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(user=request.user)
        return queryset


class UpdateProfileView(UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    queryset = UserProfile
    permission_classes = [IsAuthenticated]


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        code = str(generate_code())
        id = f'{generate_code()}{code}{"".join(choices(ascii_letters, k=4))}'
        phone = self.request.data.get('phone', '')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sms_resp = send_message_code(id, code, phone)
            user = User.objects.get(phone=phone)
            user.otp = code
            user.save()
            UserProfile.objects.create(user=user,
                                       first_name=first_name,
                                       last_name=last_name)
            return Response(
                {'phone': serializer.data.get('phone'), 'message': sms_resp},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivationView(GenericAPIView):
    permission_classes = []

    def put(self, request, *args, **kwargs):
        code = request.data.get('code', '')
        phone = request.data.get('phone', '')
        user = User.objects.get(phone=phone)
        if code:
            if code == user.otp:
                user.is_active = True
                user.save()
                return Response({'detail': 'User is successfully activated'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Code is incorrect'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Enter code'},
                            status=status.HTTP_400_BAD_REQUEST)


class RequestResetPasswordView(GenericAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        code = str(generate_code())
        id = f'{generate_code()}{code}{"".join(choices(ascii_letters, k=4))}'
        phone = request.data.get('phone', '')
        if phone:
            try:
                user = User.objects.get(phone=phone)
                user.otp = code
                send_message_code(id, code, phone)
                user.save()
                return Response({'phone': user.phone,
                                 'message': 'We sent you reset SMS. Please check the message and enter the code'},
                                status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(
                    {'detail': 'User with this phone number does not exists.'},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Enter phone number'},
                            status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = []

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password reset success'},
                        status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
