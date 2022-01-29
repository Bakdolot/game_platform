from django.urls import path, include
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

router.register('devices', FCMDeviceAuthorizedViewSet)


urlpatterns = [
    path('device/', include(router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('send/code/', UserSendCodeView.as_view()),
    path('activation/', RegisterCodeVerifyView.as_view(), name='user_activation'),
    path('password/reset/verify/', PasswordResetVerifyView.as_view(),
        name='password_reset'),
    path('phone/reset/verify/', PhoneResetVerifyView.as_view(),
        name='set_new_password'),


    path('update_profile/', UpdateProfileView.as_view(),
        name='auth_update_profile'),
    path("user/detail/", UserProfileDetailView.as_view(),
        name="profile"),
    path('user/games/statistic/', UserGamesDetailView.as_view()),
    path('get/comments/', CommentsView.as_view()),
    path('user/notification/', NotificationView.as_view(), name='user_notifications'),
    path('user/battles/', MyBattlesView.as_view()),
    path('user/score/', CreateUserScoreView.as_view()),
    path('user/comment/', CreateCommentView.as_view()),
    path('user/identification/', UserIdentificationView.as_view()),
    path('user/identification/detail/', UserIdentificationDetailView.as_view()),
]
