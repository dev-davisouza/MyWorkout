# Generated by Django 5.0.2 on 2024-02-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0007_musclegroup_slug_alter_musclegroup_origins'),
    ]

    operations = [
        migrations.AddField(
            model_name='musclegroup',
            name='slug',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]