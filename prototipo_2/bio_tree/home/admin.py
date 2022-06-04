from dataclasses import fields
from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Tag, Vida, Dominio, Reino, Filo, Classe, Ordem, Familia, Genero, Especie, SubEspecie

@admin.register(User)

class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Extra Info (custom user)", {"fields" : ("role",)}),
    )

#---------------------------------------------------------------------------------------------------------------

admin.site.register(Tag)
admin.site.register(Vida)
admin.site.register(Dominio)
admin.site.register(Reino)
admin.site.register(Filo)
admin.site.register(Classe)
admin.site.register(Ordem)
admin.site.register(Familia)
admin.site.register(Genero)
admin.site.register(Especie)
admin.site.register(SubEspecie)