from django.db import migrations

def add_default_tags(apps, schema_editor):
    Tag = apps.get_model('appeals', 'Tag')
    default_tags = [
        "Протечка воды",
        "Засор канализации",
        "Поломка лифта",
        "Электричество",
        "Отопление"
    ]
    for name in default_tags:
        Tag.objects.get_or_create(name=name)

class Migration(migrations.Migration):
    dependencies = [

        ('appeals', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_tags),
    ]