from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UserChangeForm, UserCreationForm
from .models import *

admin.site.register(image_test)
admin.site.register(Vida)
admin.site.register(Tag)
admin.site.register(Taxon)

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Other infos", {"fields": ("user_image","user_description",)}),
    )