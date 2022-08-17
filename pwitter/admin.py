from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Pweet, PweetReply
from .forms import UserCreationForm

class ProfileInline(admin.StackedInline):
    model = Profile

class PweetReplyInline(admin.StackedInline):
    model = PweetReply


class CustomUserAdmin(UserAdmin):

    add_form = UserCreationForm

    ordering = ("email",)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')
        }),
    )
    filter_horizontal = ()

    inlines = [ProfileInline]

class PweetAdmin(admin.ModelAdmin):
    model = PweetReply

    inlines = [PweetReplyInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Pweet, PweetAdmin)
admin.site.register(PweetReply)


