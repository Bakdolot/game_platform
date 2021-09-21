from django.http import request
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, get_user_model

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as filters

from .models import *
from .serializers import *
from .tasks import send_email
from accounts.models import UserProfile

from decimal import Decimal


class BattleListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ['game', 'rate', 'game__category']
    pagination_class = LimitOffsetPagination
    serializer_class = BattleListSerializer
    queryset = Battle.objects.all()


class BattleDetailView(generics.GenericAPIView):
    serializer_class = BattleEditSerializer

    def get(self, format=None, *args, **kwargs):

        battle = get_object_or_404(Battle.objects.all(), id=kwargs['id'])
        battle_user = {
            'user': get_object_or_404(get_user_model(), id=battle.owner.id),
            'user2': UserProfile.objects.get(user=battle.owner)
            }
        battle_members = BattleMembers.objects.filter(battle=battle)
        battle_list = Battle.objects.filter(game=battle.game, status='1').exclude(id=kwargs['id'])
        battle_list_serializer = SimilarBattlesSerializer(battle_list, many=True)
        battle_members_serializer = BattleMembersSerializer(battle_members, many=True)
        battle_detail_serializer = DetailBattleSerializer(battle)
        battle_user_serializer = BattleUserSerializer(battle_user)
        battle_response = battle.battle_response
        battle_response_serializer = BattleResponseSerializer(battle_response)

        return Response({
            'battle_list_serializer' : battle_list_serializer.data,
            'battle_members_serializer' : battle_members_serializer.data,
            'battle_detail_serializer' : battle_detail_serializer.data,
            'battle_user_serializer' : battle_user_serializer.data,
            'battle_response' : battle_response_serializer.data,
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if request.data['owner'] == request.user:
            serializer = BattleEditSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        battle = get_object_or_404(Battle.objects.all(), id=kwargs['id'])
        if self.request.user == battle.owner:
            user = UserProfile.objects.get(user=self.request.user)
            user.balance += Decimal(battle.rate)
            user.save()
            battle.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class GameView(generics.ListAPIView):
    serializer_class = AllBattlesSerializer
    queryset = Game.objects.all()


class DetailGameView(generics.GenericAPIView):

    def get(self, format=None, *args, **kwargs):
        # games = Game.objects.filter(id=kwargs['id']).first()
        games = get_object_or_404(Game.objects.all(), id=kwargs['id'])
        battles = Battle.objects.filter(game=games, status='1')
        games_serializer = AllBattlesSerializer(games)
        battles_serializer = SimilarBattlesSerializer(battles, many=True)

        return Response({
            'games' : games_serializer.data,
            'battles' : battles_serializer.data,
        }, status=status.HTTP_200_OK)


class DetailGameView2(generics.GenericAPIView):

    def get(self, format=None, *args, **kwargs):
        # games = Game.objects.filter(id=kwargs['id']).first()
        games = get_object_or_404(Game.objects.all(), id=kwargs['id'])
        battles = Battle.objects.filter(game=games, status='1')
        games_serializer = AllBattlesSerializer(games)
        battles_serializer = GameBattlesSerializer(battles, many=True)

        return Response({
            'games' : games_serializer.data,
            'battles' : battles_serializer.data,
        }, status=status.HTTP_200_OK)



class FollowToGame(generics.GenericAPIView):
    def post(self):
        game = Game.objects.get(id=self.request.data['game_id'])
        user = self.request.user
        if request.data['type'] == 'follow':    
            if user not in game.followers.all():
                game.followers.add(user=user)
                return Response(status=status.HTTP_202_ACCEPTED)
        elif request.data['type'] == 'unfollow':
            if user in game.followers.all():
                game.followers.delete(user=user)
                return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_200_OK)


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CreateBattleView(generics.CreateAPIView):
    serializer_class = CreateBattleSerializer

    def create(self, request, *args, **kwargs):
        data = {}
        data.update(request.data)
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        profile = UserProfile.objects.get(user=request.user)
        if int(request.data['rate']) > profile.balance:
            return Response({
                'Not enough of balance': 'User doesnt have enough the balance'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        profile.balance -= int(request.data['rate'])
        profile.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateBattleMembersView(generics.CreateAPIView):
    serializer_class = CreateBattleMembersSerializer


class QuestionView(generics.CreateAPIView):
    serializer_class = QuestionsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        text = f"""
        email ->  {serializer.data['email']}
        text  ->  {serializer.data['text']}
        """
        send_email.apply_async((text, ))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MainBattleResponseView(generics.CreateAPIView):
    serializer_class = MainBattleResponseSerializer


