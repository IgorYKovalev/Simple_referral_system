from django.db import models
from app_auth.models import CustomUser


class ReferralUser(models.Model):
    i_invited = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='меня пригласили',
        related_name='referred'
    )

    he_invited_me = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='я пригласил',
        related_name='referrer'
    )

    def __str__(self):
        return f'{self.i_invited}'

    class Meta:
        verbose_name_plural = 'реферальная ссылка'
