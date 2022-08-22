# Generated by Django 4.0.6 on 2022-08-19 13:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=140)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pweet_image', models.FileField(blank=True, upload_to='pweet_media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])])),
                ('likes', models.ManyToManyField(blank=True, related_name='pweet_posts', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pweets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PweetReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_body', models.CharField(max_length=140)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='pweet_replies', to=settings.AUTH_USER_MODEL)),
                ('pweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='pwitter.pweet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pweets_reply', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_image', models.FileField(blank=True, upload_to='profile_pictures/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])])),
                ('follows', models.ManyToManyField(blank=True, related_name='followed_by', to='pwitter.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.FileField(blank=True, upload_to='pweet_media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])])),
                ('pweet', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='pwitter.pweet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
