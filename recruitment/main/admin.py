from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class UsersAdmin(UserAdmin):
    model = Users
    list_display = ('email', 'first_name', 'last_name', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_name')}),
        ('User Config', {'fields': ('user_category_id', 'user_privilege_id')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    list_display = ("user_name", "email", "first_name", "last_name", )
    list_filter = ("is_superuser",  "groups")
    ordering = ("user_name",)

class CandidatesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Users, UsersAdmin)
admin.site.register(Candidate, CandidatesAdmin)
