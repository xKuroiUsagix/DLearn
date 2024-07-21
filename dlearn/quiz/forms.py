from django import forms
from django.forms import fields

from .models import Quiz


class QuizForm(forms.ModelForm):
    
    class Meta:
        model = Quiz
        fields = '__all__'
