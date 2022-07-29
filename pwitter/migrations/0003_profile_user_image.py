# Generated by Django 4.0.6 on 2022-07-29 11:29

from django.db import migrations, models
import pwitter.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pwitter', '0002_pweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_image',
            field=models.FileField(blank=True, upload_to='profile_pictures/', validators=[pwitter.validators.FileValidator(content_types=('profile_pictures/jgp',), max_size=102400)]),
        ),
    ]
