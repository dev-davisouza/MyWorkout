# Generated by Django 5.0.2 on 2024-03-14 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0022_setexerciserelationship_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setexerciserelationship',
            name='final_margin_expected_reps',
            field=models.IntegerField(blank=True, null=True, verbose_name='Max. of reps: (opcional)'),
        ),
        migrations.AlterField(
            model_name='setexerciserelationship',
            name='initial_margin_expected_reps',
            field=models.IntegerField(blank=True, null=True, verbose_name='Min. of reps: (opcional)'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
