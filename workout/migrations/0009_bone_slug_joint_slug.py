# Generated by Django 5.0.2 on 2024-02-20 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0008_musclegroup_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='bone',
            name='slug',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='joint',
            name='slug',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
