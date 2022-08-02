# Generated by Django 4.0.6 on 2022-07-29 11:30

from django.db import migrations, models
import pwitter.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pwitter', '0003_profile_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_image',
            field=models.FileField(blank=True, upload_to='profile_pictures/', validators=[pwitter.validators.FileValidator(content_types=('profile_pictures/jpg',), max_size=102400)]),
        ),
    ]