from django.contrib.auth.backends import ModelBackend
from app_auth.models import CustomUser


class UserModelBackend(ModelBackend):

    def authenticate(self, request, phone_number=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
