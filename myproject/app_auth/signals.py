import random
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def update_password_phone(sender, user, request, **kwargs):
    """ Генерация нового одноразового пароля """
    new_password_phone = random.randint(1000, 9999)
    user.password_phone = new_password_phone
    user.save()
