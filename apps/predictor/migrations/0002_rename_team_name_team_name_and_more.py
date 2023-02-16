# Generated by Django 4.0.5 on 2022-06-05 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='team_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='player',
            name='injury_states',
        ),
        migrations.RemoveField(
            model_name='playerfixture',
            name='now_injury_status',
        ),
        migrations.AddField(
            model_name='team',
            name='short_name',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
    ]