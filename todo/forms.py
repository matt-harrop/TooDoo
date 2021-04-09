from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import ToDo


class ToDoCreationForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'memo', 'important']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'memo': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4'
                }
            ),
            'important': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            )
        }