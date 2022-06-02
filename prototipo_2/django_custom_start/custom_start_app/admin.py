from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UserChangeForm, UserCreationForm
from .models import *


admin.site.register(image_test)
admin.site.register(Taxon)
admin.site.register(Vida)

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Campos personalizados", {"fields": ("new_field",)}),
    )