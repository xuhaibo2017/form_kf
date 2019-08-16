__author__ = 'xuhb'
from .models import  User
from django import forms

class UserListForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
          'username': forms.TextInput(attrs={'class': 'form-control'}),
          'password': forms.TextInput(attrs={'class': 'form-control'}),

        }
