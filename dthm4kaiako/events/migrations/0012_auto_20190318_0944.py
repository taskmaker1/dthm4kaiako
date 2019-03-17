# Generated by Django 2.1.5 on 2019-03-17 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_event_featured'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['region', 'city', 'name']},
        ),
        migrations.AlterModelOptions(
            name='organiser',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='sponsor',
            options={'ordering': ['name']},
        ),
    ]
