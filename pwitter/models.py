from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


from .validators import FileValidator


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    validate_file = FileValidator(max_size=1024 * 1000,
                                  content_types=('image/jpeg', 'image/png'))
    picture = models.FileField(upload_to='pweet_media/',
                             validators=[validate_file],
                             blank=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, null=True,
                                blank=True)
    creates = models.DateTimeField(auto_now_add=True)


class Pweet(models.Model):
    user = models.ForeignKey(User, related_name="pweets",
                             on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    validate_file = FileValidator(max_size=1024 * 1000,
                                  content_types=('image/jpeg', 'image/png'))
    pweet_image = models.FileField(upload_to='pweet_media/',
                                  validators=[validate_file],
                                  blank=True)
    picture = models.OneToOneField(Picture, on_delete=models.DO_NOTHING, null=True,
                                   )


    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )


class PweetReply(models.Model):
    user = models.ForeignKey(User, related_name="pweets_reply",
                             on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.OneToOneField(Picture, on_delete=models.DO_NOTHING, null=True,
                                   blank=True)
    reply = models.ForeignKey(Pweet, on_delete=models.DO_NOTHING, related_name='replies')


    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    validate_file = FileValidator(max_size=1024*1000,
                                  content_types=('image/jpeg', 'image/png'))
    user_image = models.FileField(upload_to='profile_pictures/',
                                  validators=[validate_file],
                                  blank=True)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        # user_profile.follows.set([instance.profile.id])
        user_profile.save()


