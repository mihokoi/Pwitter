# Generated by Django 4.0.6 on 2022-08-04 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pwitter', '0012_alter_pweet_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pweet',
            name='picture',
        ),
        migrations.AddField(
            model_name='picture',
            name='pweet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pwitter.pweet'),
        ),
    ]
