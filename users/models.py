from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_active', True)

        if not phone:
            raise ValueError('Superuser must have a phone number')
        return self._create_user(username, email, password, phone, **extra_fields)

    def create_staffuser(self, username, email, password, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'staff')
        extra_fields.setdefault('is_active', True)

        if not phone:
            raise ValueError('Staff user must have a phone number')
        return self._create_user(username, email, password, phone, **extra_fields)

    def create_user(self, username, email, password, phone, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'user')
        return self._create_user(username, email, password, phone, **extra_fields)

    def _create_user(self, username, email, password, phone, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone number')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    ROLES = (
        ('user', _('Обычный пользователь')),
        ('staff', _('Сотрудник')),
        ('admin', _('Администратор')),
    )

    role = models.CharField(
        _('Роль'),
        max_length=20,
        choices=ROLES,
        default='user'
    )

    phone_regex = RegexValidator(
        regex=r'^\+7\d{10}$',
        message=_("Номер телефона должен быть в формате: '+79999999999'.")
    )
    phone = models.CharField(
        _('Телефон'),
        max_length=12,
        validators=[phone_regex],
        unique=True
    )

    email = models.EmailField(
        _('Email'),
        unique=True,
        max_length=254,
        validators=[
            MaxLengthValidator(254, message="Максимальная длина email - 254 символа")
        ]
    )

    first_name = models.CharField(
        _('Имя'),
        max_length=150,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁa-zA-Z\s\-]+$',
                message="Имя может содержать только буквы и дефисы"
            )
        ]
    )

    last_name = models.CharField(
        _('Фамилия'),
        max_length=150,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁa-zA-Z\s\-]+$',
                message="Фамилия может содержать только буквы и дефисы"
            )
        ]
    )

    username = models.CharField(
        _('Логин'),
        max_length=30,
        unique=True,
        validators=[
            MinLengthValidator(4, message="Логин должен содержать минимум 4 символа"),
            MaxLengthValidator(30, message="Максимальная длина логина - 30 символов"),
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message="Логин может содержать только буквы, цифры и символы @/./+/-/_"
            )
        ]
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Comment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    text = models.TextField(
        'Текст комментария',
        validators=[
            MinLengthValidator(10, message="Комментарий должен содержать минимум 10 символов"),
            MaxLengthValidator(1000, message="Максимальная длина комментария - 1000 символов")
        ]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    is_edited = models.BooleanField('Редактировался', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author.username}'