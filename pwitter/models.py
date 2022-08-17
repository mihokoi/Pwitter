import os.path

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# from .validators import FileValidator
from django.core.validators import FileExtensionValidator


class Pweet(models.Model):
    user = models.ForeignKey(User, related_name="pweets",
                             on_delete=models.CASCADE)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    # validate_file = FileValidator(max_size=1024 * 1000,
    #                               content_types=('image/jpeg', 'image/png'))
    pweet_image = models.FileField(upload_to='pweet_media/',
                                  validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
                                  blank=True)
    likes = models.ManyToManyField(User, related_name='pweet_posts', blank=True)
    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )


class PweetReply(models.Model):
    user = models.ForeignKey(User, related_name="pweets_reply",
                             on_delete=models.DO_NOTHING)
    reply_body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    pweet = models.ForeignKey(Pweet, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(User, related_name='pweet_replies', blank=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.reply_body[:30]}..."
        )



class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # validate_file = FileValidator(max_size=1024 * 1000,
    #                                   content_types=('image/jpeg', 'image/png'))
    picture = models.FileField(upload_to='pweet_media/',
                                   validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
                                   blank=True)
    pweet = models.OneToOneField(Pweet, on_delete=models.CASCADE, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    user_image = models.FileField(upload_to='profile_pictures/',
                                  validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
                                  blank=True)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username


@receiver(models.signals.post_delete, sender=Pweet)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.pweet_image:
        if os.path.isfile(instance.pweet_image.path):
            os.remove(instance.pweet_image.path)


@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.user_image:
        if os.path.isfile(instance.user_image.path):
            os.remove(instance.user_image.path)


@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_picture = Profile.objects.get(pk=instance.pk).user_image
    except Picture.DoesNotExist:
        return False

    new_picture = instance.user_image
    if not old_picture == new_picture:
        try:
            if os.path.isfile(old_picture.path):
                os.remove(old_picture.path)
        except ValueError:
            return False




@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        # user_profile.follows.set([instance.profile.id])
        user_profile.save()



