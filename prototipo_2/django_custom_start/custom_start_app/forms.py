from django.contrib.auth import forms as uforms
from django import forms
from .models import *

class UserChangeForm(uforms.UserChangeForm):
    class Meta(uforms.UserChangeForm.Meta):
        model = User

class UserCreationForm(uforms.UserCreationForm):
    class Meta(uforms.UserCreationForm.Meta):
        model = User

class image_testForm(forms.ModelForm):
    class Meta:
        model = image_test
        fields = ['name', 'image']