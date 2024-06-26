# Generated by Django 5.0.2 on 2024-03-11 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0018_setexerciserelationship_workout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Workout name'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='set_exercise_relationships',
            field=models.ManyToManyField(blank=True, to='workout.setexerciserelationship'),
        ),
    ]
