from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('appeals', '0008_alter_comment_author'),
    ]

    operations = [
        # Сначала создаем новые модели
        migrations.CreateModel(
            name='AppealStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('code', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Статус обращения',
                'verbose_name_plural': 'Статусы обращений',
            },
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('code', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Приоритет',
                'verbose_name_plural': 'Приоритеты',
            },
        ),
        migrations.CreateModel(
            name='EmployeeStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('code', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Статус сотрудника',
                'verbose_name_plural': 'Статусы сотрудников',
            },
        ),

        # Добавляем новые ForeignKey поля как NULL
        migrations.AddField(
            model_name='appeal',
            name='status_link',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='appeals.AppealStatus',
                verbose_name='Статус'
            ),
        ),
        migrations.AddField(
            model_name='appeal',
            name='priority_link',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='appeals.Priority',
                verbose_name='Приоритет'
            ),
        ),
        migrations.AddField(
            model_name='appeal',
            name='employee_status_link',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='appeals.EmployeeStatus',
                verbose_name='Статус для сотрудников'
            ),
        ),
    ]