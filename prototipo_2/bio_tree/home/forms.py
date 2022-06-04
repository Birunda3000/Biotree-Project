from dataclasses import field
from django.contrib.auth import forms

from .models import User, Tag, Vida, Dominio, Reino, Filo, Classe, Ordem, Familia, Genero, Especie, SubEspecie

from django.forms import ModelForm

class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User

class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User

class VidaForm(ModelForm):
    class Meta:
        model = Vida
        fields = ['nome','origem','extinção','descrição','description_language_II','antepassados','image','image_2','image_3','tags']#'data_criação',
