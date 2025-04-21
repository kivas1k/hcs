from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+7\d{10}$',
        message="Номер телефона должен быть в формате: '+79999999999'."
    )
    phone = models.CharField(
        'Телефон',
        max_length=12,
        validators=[phone_regex],
        unique=True
    )

    first_name = models.CharField('Имя', max_length=150, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True, null=True)
    email = models.EmailField('Email', unique=True, blank=True, null=True)

    def __str__(self):
        return self.username
