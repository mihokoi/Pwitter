from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Profile, Pweet, PweetReply


class ProfileInline(admin.StackedInline):
    model = Profile

class PweetReplyInline(admin.StackedInline):
    model = PweetReply


class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username"]
    inlines = [ProfileInline]

class PweetAdmin(admin.ModelAdmin):
    model = PweetReply

    inlines = [PweetReplyInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Pweet, PweetAdmin)
admin.site.register(PweetReply)


