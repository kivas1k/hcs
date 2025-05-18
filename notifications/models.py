from django.db import models
from django.contrib.auth import get_user_model
from appeals.models import Appeal

User = get_user_model()

class UnreadNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('status_change', 'Изменение статуса'),
        ('priority_change', 'Изменение приоритета'),
        ('tag_change', 'Изменение тегов'),
        ('comment', 'Новый комментарий'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    unread = UnreadNotificationManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Уведомление для {self.user.username} ({self.get_notification_type_display()})"

    def mark_as_read(self):
        self.is_read = True
        self.save()