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

    EMPLOYEE_STATUS_CHOICES = [
        ('free', 'Свободное'),
        ('in_progress', 'В работе'),
        ('closed', 'Закрыто'),
    ]

    employee_status = models.CharField(
        max_length=20,
        choices=EMPLOYEE_STATUS_CHOICES,
        default='free',
        verbose_name='Статус для сотрудников'
    )
    taken_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='taken_appeals',
        verbose_name='Взял сотрудник'
    )
    closed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='closed_appeals',
        verbose_name='Закрыл сотрудник'
    )
    taken_at = models.DateTimeField(null=True, blank=True, verbose_name='Взято в работу')
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата закрытия')
    rating = models.PositiveIntegerField(
        'Оценка',
        null=True,
        blank=True,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )
    feedback_comment = models.TextField('Комментарий оценки', null=True, blank=True)
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    address = models.CharField('Адрес проживания', max_length=200, blank=True)
    full_name = models.CharField('ФИО', max_length=150, blank=True)
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

class Comment(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author.username} к обращению {self.appeal.id}'

    def is_staff_comment(self):
        return self.author.role in ['staff', 'admin']