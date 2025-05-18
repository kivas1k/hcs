from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from appeals.models import Appeal, Comment
from .models import Notification

User = get_user_model()


@receiver(post_save, sender=Appeal)
def handle_appeal_changes(sender, instance, **kwargs):
    if kwargs.get('created'):
        return

    if instance._original_status != instance.status:
        Notification.objects.create(
            user=instance.author,
            appeal=instance,
            notification_type='status_change',
            message=f'Статус вашего обращения "{instance.title}" изменен на "{instance.status.name}"'
        )

    if instance._original_priority != instance.priority:
        Notification.objects.create(
            user=instance.author,
            appeal=instance,
            notification_type='priority_change',
            message=f'Приоритет вашего обращения "{instance.title}" изменен на "{instance.priority.name}"'
        )


@receiver(m2m_changed, sender=Appeal.tags.through)
def handle_tags_change(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        current_tags = set(instance.tags.all())
        if instance._original_tags != current_tags:
            Notification.objects.create(
                user=instance.author,
                appeal=instance,
                notification_type='tag_change',
                message=f'Теги вашего обращения "{instance.title}" были изменены'
            )


@receiver(post_save, sender=Comment)
def handle_new_comment(sender, instance, created, **kwargs):
    if created and instance.appeal.author and instance.author != instance.appeal.author:
        Notification.objects.create(
            user=instance.appeal.author,
            appeal=instance.appeal,
            notification_type='comment',
            message=f'Новый комментарий к вашему обращению "{instance.appeal.title}"'
        )