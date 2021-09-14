from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *


urlpatterns = [
    path("create/fcm", FcmCreateView.as_view(), name="fcm-create"),
    path("profile/detail/<int:pk>", UserProfileDetailView.as_view(),
         name="profile"),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(),
         name='auth_update_profile'),
     path('user/notification/', NotificationView.as_view(), name='user_notifications'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('activation/', UserActivationView.as_view(), name='user_activation'),
    path('password_reset/', RequestResetPasswordView.as_view(),
         name='password_reset'),
    path('set_new_password/', SetNewPasswordView.as_view(),
         name='set_new_password'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(),
         name='change_password'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
