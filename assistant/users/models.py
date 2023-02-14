from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    tg_chat_id = models.BigIntegerField(verbose_name='Чат ID', unique=True, null=True, blank=True)
    tg_username = models.CharField(max_length=255, default='', verbose_name='Telegram username', blank=True)
    tg_first_name = models.CharField(max_length=255, default='', verbose_name='Telegram first_name', blank=True)
    tg_last_name = models.CharField(max_length=255, default='', verbose_name='Telegram last_name', blank=True)
    comments = models.CharField(max_length=255, default='', verbose_name='Комментарий', blank=True)
    setting_task_title = models.BooleanField(default=True, blank=True, verbose_name='Реквизиты задачи')
    setting_task_sorting = models.CharField(max_length=255, default='date_created_ASC', blank=True,
                                            verbose_name='Telegram type sort')
    setting_screenshot = models.BooleanField(default=False, blank=True, verbose_name='Скриншот обновления')
    date_UPD = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', blank=True)

    def __str__(self):
        return self.username

