# Generated by Django 4.0.6 on 2022-08-04 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pwitter', '0013_remove_pweet_picture_picture_pweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='pweet',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='pwitter.pweet'),
        ),
    ]