from django.db import models
from users.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, MaxValueValidator

class FAQCategory(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=100,
        validators=[
            MinLengthValidator(
                3,
                message="Название должно содержать минимум 3 символа"
            ),
            MaxLengthValidator(
                100,
                message="Максимальная длина названия - 100 символов"
            ),
            RegexValidator(
                regex=r'^[а-яА-ЯёЁa-zA-Z0-9\s\-_]+$',
                message="Допустимы буквы, цифры, пробелы, дефисы и подчеркивания"
            )
        ]
    )
    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0,
        validators=[
            MaxValueValidator(
                1000,
                message="Максимальное значение порядка - 1000"
            )
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Категория FAQ'
        verbose_name_plural = 'Категории FAQ'
        ordering = ['order']

    def __str__(self):
        return self.name

class FAQItem(models.Model):
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='questions'
    )
    question = models.CharField(
        'Вопрос',
        max_length=255,
        validators=[
            MinLengthValidator(
                10,
                message="Вопрос должен содержать минимум 10 символов"
            ),
            RegexValidator(
                regex=r'^[а-яА-ЯёЁa-zA-Z0-9\s\-\?\.!,]+$',
                message="Допустимы буквы, цифры и основные знаки препинания"
            )
        ]
    )
    answer = models.TextField(
        'Ответ',
        validators=[
            MinLengthValidator(
                10,
                message="Ответ должен содержать минимум 20 символов"
            ),
            MaxLengthValidator(
                5000,
                message="Максимальная длина ответа - 5000 символов"
            )
        ]
    )
    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0,
        validators=[
            MaxValueValidator(
                1000,
                message="Максимальное значение порядка - 1000"
            )
        ]
    )
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'
        ordering = ['category__order', 'order']

    def __str__(self):
        return self.question[:50] + '...' if len(self.question) > 50 else self.question