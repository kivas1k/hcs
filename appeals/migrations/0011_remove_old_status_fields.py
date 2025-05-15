from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('appeals', '0010_convert_statuses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appeal',
            name='status',
        ),
        migrations.RemoveField(
            model_name='appeal',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='appeal',
            name='employee_status',
        ),
        migrations.RenameField(
            model_name='appeal',
            old_name='status_link',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='appeal',
            old_name='priority_link',
            new_name='priority',
        ),
        migrations.RenameField(
            model_name='appeal',
            old_name='employee_status_link',
            new_name='employee_status',
        ),
    ]