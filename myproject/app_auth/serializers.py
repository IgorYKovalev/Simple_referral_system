from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import CustomUser


phone_regex = RegexValidator(
    regex=r'^\+?7?\d{10}$',
    message='Введите допустимое значение'
)


class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex])

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'invite_code']
