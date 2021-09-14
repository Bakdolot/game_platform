from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as filters
from accounts.models import UserProfile


class BattleListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ['game', 'rate', 'game__category']
    pagination_class = LimitOffsetPagination
    serializer_class = BattleListSerializer
    queryset = Battle.objects.all()


# class BattleDetailView(generics.GenericAPIView):

#     def get(self, format=None, *args, **kwargs):

#         battle = get_object_or_404(Battle.objects.all(), id=kwargs['id'])
#         battle_user = UserProfile.objects.get(user=battle.owner)
#         battle_members = BattleMembers.objects.get(battle=battle)
#         battle_list = Battle.objects.filter(game=battle.game, status='1')
#         battle_list_serializer = SimilarBattlesSerializer(battle_list, many=True)
#         battle_members_serializer = BattleMembersSerializer(battle_members)
#         battle_detail_serializer = DetailBattleSerializer(battle)
#         battle_user_serializer = BattleUserSerializer(battle_user)

#         return Response({
#             'battle_list_serializer' : battle_list_serializer.data,
#             'battle_members_serializer' : battle_members_serializer.data,
#             'battle_detail_serializer' : battle_detail_serializer.data,
#             'battle_user_serializer' : battle_user_serializer.data,
#         }, status=status.HTTP_200_OK)


class BattleDetailView(generics.GenericAPIView):

    def get(self, format=None, *args, **kwargs):

        battle = get_object_or_404(Battle.objects.all(), id=kwargs['id'])
        battle_user = {
            'user': get_object_or_404(get_user_model(), id=battle.owner.id),
            'user2': UserProfile.objects.get(user=battle.owner)
            }
        battle_members = BattleMembers.objects.get(battle=battle)
        battle_list = Battle.objects.filter(game=battle.game, status='1')
        battle_list_serializer = SimilarBattlesSerializer(battle_list, many=True)
        battle_members_serializer = BattleMembersSerializer(battle_members)
        battle_detail_serializer = DetailBattleSerializer(battle)
        battle_user_serializer = BattleUserSerializer(battle_user)

        return Response({
            'battle_list_serializer' : battle_list_serializer.data,
            'battle_members_serializer' : battle_members_serializer.data,
            'battle_detail_serializer' : battle_detail_serializer.data,
            'battle_user_serializer' : battle_user_serializer.data,
        }, status=status.HTTP_200_OK)



class CategoryView(generics.ListAPIView):
    serializer_class = AllBattlesSerializer
    queryset = Game.objects.all()


class DetailCategoryView(generics.GenericAPIView):

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


class DetailCategoryView2(generics.GenericAPIView):

    def get(self, format=None, *args, **kwargs):
        # games = Game.objects.filter(id=kwargs['id']).first()
        games = get_object_or_404(Game.objects.all(), id=kwargs['id'])
        battles = Battle.objects.filter(game=games, status='1')
        games_serializer = AllBattlesSerializer(games)
        battles_serializer = CategoryBattlesSerializer(battles, many=True)

        return Response({
            'games' : games_serializer.data,
            'battles' : battles_serializer.data,
        }, status=status.HTTP_200_OK)