from django.contrib import admin

from .models import Cart
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone_number', 'name', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'name')}),
    )
    ordering = ('phone_number',)

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Cart)
# Register your models here.
