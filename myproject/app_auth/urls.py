from django.urls import path
from .api import (
    RegisterUserAPIView,
    VerifyUserAPIView,
    UserProfileAPIView,
    ActivateInviteCodeAPIView,
    InvitedUsersAPIView,
)

app_name = 'app_auth'

urlpatterns = [
    path('v1/register/', RegisterUserAPIView.as_view(), name='register'),
    path('v1/verify/', VerifyUserAPIView.as_view(), name='verify'),
    path('v1/profile/', UserProfileAPIView.as_view(), name='profile'),
    path('v1/activate_invite_code/', ActivateInviteCodeAPIView.as_view(), name='activate_invite_code'),
    path('v1/invited_users/', InvitedUsersAPIView.as_view(), name='invited_users'),
]
