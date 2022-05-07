from django import forms
from django.forms import widgets

from .models import Task


class TaskForm(forms.ModelForm):
    
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))
    do_up_to = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'дд/мм/рррр гг/хх'
        })
    )
    
    class Meta:
        model = Task
        exclude = ('course', 'has_quiz')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'назва'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'опис завдання'}),
        }
