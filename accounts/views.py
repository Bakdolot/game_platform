from xml.dom.minidom import Comment
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, filters, permissions

from .utils import send_message_code, generate_code
from .models import *
from .serializers import *
from accounts.tasks import cheking_acc
from main.models import BattleResponse, Game

from random import choices
from string import ascii_letters


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User
    

class UserSendCodeView(GenericAPIView):
    serializer_class = UserSendCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_otp_code()
        return Response(status=status.HTTP_202_ACCEPTED)


class RegisterCodeVerifyView(GenericAPIView):
    serializer_class = RegisterCodeVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update()
        return Response(status=status.HTTP_202_ACCEPTED)


class PasswordResetVerifyView(GenericAPIView):
    serializer_class = PasswordResetVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update()
        return Response(status=status.HTTP_202_ACCEPTED)


class PhoneResetVerifyView(GenericAPIView):
    serializer_class = PhoneResetVerifySerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_object(self):
        return self.request.user

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=self.get_object())
        return Response(status=status.HTTP_202_ACCEPTED)


class AllUsersView(ListAPIView):
    serializer_class = AllUsersSerializer
    queryset = UserProfile.objects.filter(user__is_active=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'first_name', 'last_name']


class UserProfileDetailView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        return queryset
    

class CommentsView(ListAPIView):
    serializer_class = CreateCommentSerializer
    
    def get_queryset(self):
        queryset = UserComment.objects.filter(user=self.request.user)
        return queryset


class UserGamesDetailView(ListAPIView):
    serializer_class = UserGameResultsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = BattleHistory.objects.filter(followers=self.request.user)
        return queryset


class CreateUserScoreView(CreateAPIView):
    serializer_class = CreateScoreUserSerializer
    queryset = UserScores
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        profile = UserProfile.objects.get(id=request.data['user'])
        if request.data['type'] == '1':
            profile.courtesy_rate_sum += request.data['score']
        elif request.data['type'] == '2':
            profile.punctuality_rate_sum += request.data['score']
        elif request.data['type'] == '3':
            profile.adequacy_rate_sum += request.data['score']
        profile.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateCommentView(CreateAPIView):
    serializer_class = CreateCommentSerializer
    queryset = UserComment.objects.all()
    permission_classes = [IsAuthenticated]


class MyBattlesView(ListAPIView):
    serializer_class = UserBattlesSerializer

    def get_queryset(self):
        type = self.request.data['type']
        if type == 'owner':
            queryset = Battle.objects.filter(owner=self.request.user)
        elif type == 'response':
            queryset = BattleResponse.objects.filter(owner=self.request.user)
        return queryset


class UserIdentificationView(CreateAPIView):
    serializer_class = UserIdentificationSerializer
    queryset = Identification.objects.all()
    permission_classes = [IsAuthenticated]


class UserIdentificationDetailView(RetrieveAPIView):
    serializer_class = UserIdentificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Identification.objects.filter(user=self.request.user)
        return queryset
        

class NotificationView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        return queryset


class UpdateProfileView(UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        return queryset
