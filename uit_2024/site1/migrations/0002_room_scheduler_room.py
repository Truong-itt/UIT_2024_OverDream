# Generated by Django 5.1 on 2024-09-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='scheduler_room',
            field=models.ManyToManyField(blank=True, to='site1.scheduler_room'),
        ),
    ]
