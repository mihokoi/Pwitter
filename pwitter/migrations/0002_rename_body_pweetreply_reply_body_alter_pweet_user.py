# Generated by Django 4.0.6 on 2022-08-17 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pwitter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pweetreply',
            old_name='body',
            new_name='reply_body',
        ),
        migrations.AlterField(
            model_name='pweet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pweets', to=settings.AUTH_USER_MODEL),
        ),
    ]