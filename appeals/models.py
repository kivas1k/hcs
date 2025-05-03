from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class Appeal(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    address = models.CharField('Адрес проживания', max_length=200, blank=True)  # Необязательное
    full_name = models.CharField('ФИО', max_length=150, blank=True)            # Необязательное
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField('Приоритет', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appeals')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)

    def __str__(self):
        return self.title

class AppealDocument(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='appeals/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.appeal.title}"

