from django.db import migrations


def convert_statuses(apps, schema_editor):
    Appeal = apps.get_model('appeals', 'Appeal')
    AppealStatus = apps.get_model('appeals', 'AppealStatus')
    Priority = apps.get_model('appeals', 'Priority')
    EmployeeStatus = apps.get_model('appeals', 'EmployeeStatus')

    # Создаем статусы, если их еще нет
    status_new, _ = AppealStatus.objects.get_or_create(code='new', defaults={'name': 'Новое'})
    status_in_progress, _ = AppealStatus.objects.get_or_create(code='in_progress', defaults={'name': 'В работе'})
    status_completed, _ = AppealStatus.objects.get_or_create(code='completed', defaults={'name': 'Завершено'})

    priority_low, _ = Priority.objects.get_or_create(code='low', defaults={'name': 'Низкий'})
    priority_medium, _ = Priority.objects.get_or_create(code='medium', defaults={'name': 'Средний'})
    priority_high, _ = Priority.objects.get_or_create(code='high', defaults={'name': 'Высокий'})

    emp_status_free, _ = EmployeeStatus.objects.get_or_create(code='free', defaults={'name': 'Свободное'})
    emp_status_in_progress, _ = EmployeeStatus.objects.get_or_create(code='in_progress', defaults={'name': 'В работе'})
    emp_status_closed, _ = EmployeeStatus.objects.get_or_create(code='closed', defaults={'name': 'Закрыто'})

    # Обновляем существующие записи Appeal
    for appeal in Appeal.objects.all():
        # Конвертируем статус
        if appeal.status == 'new':
            appeal.status_link = status_new
        elif appeal.status == 'in_progress':
            appeal.status_link = status_in_progress
        elif appeal.status == 'completed':
            appeal.status_link = status_completed

        # Конвертируем приоритет
        if appeal.priority == 'low':
            appeal.priority_link = priority_low
        elif appeal.priority == 'medium':
            appeal.priority_link = priority_medium
        elif appeal.priority == 'high':
            appeal.priority_link = priority_high

        # Конвертируем статус сотрудника
        if appeal.employee_status == 'free':
            appeal.employee_status_link = emp_status_free
        elif appeal.employee_status == 'in_progress':
            appeal.employee_status_link = emp_status_in_progress
        elif appeal.employee_status == 'closed':
            appeal.employee_status_link = emp_status_closed

        appeal.save()


class Migration(migrations.Migration):
    dependencies = [
        ('appeals', '0009_appealstatus_employeestatus_priority_and_more'),
    ]

    operations = [
        migrations.RunPython(convert_statuses),
    ]