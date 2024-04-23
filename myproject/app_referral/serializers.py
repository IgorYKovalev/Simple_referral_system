from rest_framework import serializers
from .models import ReferralUser
from app_auth.serializers import CustomUserSerializer


class ReferralUserSerializer(serializers.ModelSerializer):
    i_invited = CustomUserSerializer()
    he_invited_me = CustomUserSerializer()

    class Meta:
        model = ReferralUser
        fields = ['id', 'i_invited', 'he_invited_me']
