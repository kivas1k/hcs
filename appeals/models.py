from django.db import models
from users.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.validators import RegexValidator

class Tag(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class AppealStatus(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    code = models.CharField('Код', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Статус обращения'
        verbose_name_plural = 'Статусы обращений'

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    code = models.CharField('Код', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'

    def __str__(self):
        return self.name

class EmployeeStatus(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    code = models.CharField('Код', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Статус сотрудника'
        verbose_name_plural = 'Статусы сотрудников'

    def __str__(self):
        return self.name

class Appeal(models.Model):
    employee_status = models.ForeignKey(
        EmployeeStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[RegexValidator(regex=r'^\+7\d{10}$')],
        blank=True
    )
    status = models.ForeignKey(
        AppealStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Статус'
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Приоритет'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appeals')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status
        self._original_priority = self.priority

    @classmethod
    def get_default_employee_status(cls):
        status, _ = EmployeeStatus.objects.get_or_create(
            code='free',
            defaults={'name': 'Свободно'}
        )
        return status

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.employee_status_id:
            self.employee_status = self.get_default_employee_status()
        super().save(*args, **kwargs)
        self._original_status = self.status
        self._original_priority = self.priority
        self._original_tags = set(self.tags.all())

    @property
    def status_code(self):
        return self.status.code if self.status else None

    @property
    def priority_code(self):
        return self.priority.code if self.priority else None

    @property
    def employee_status_code(self):
        return self.employee_status.code if self.employee_status else None

class AppealDocument(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='appeals/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.appeal.title}"

class Comment(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appeal_comments')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author.username} к обращению {self.appeal.id}'

    def is_staff_comment(self):
        return self.author.role in ['staff', 'admin']