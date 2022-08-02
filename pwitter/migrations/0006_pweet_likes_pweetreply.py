# Generated by Django 4.0.6 on 2022-07-29 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pwitter.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pwitter', '0005_pweet_media_alter_profile_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pweet',
            name='likes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.CreateModel(
            name='PweetReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=140)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('media', models.FileField(blank=True, upload_to='pweet_media/', validators=[pwitter.validators.FileValidator(content_types=('image/jpeg', 'image/png'), max_size=1024000)])),
                ('likes', models.IntegerField(blank=True, default=0)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='replies', to='pwitter.pweet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pweets_reply', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]