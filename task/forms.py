from django import forms
from django.forms.utils import ErrorList
from django.utils import timezone
from django.forms import widgets

from datetime import datetime

from .models import Task


class TaskForm(forms.ModelForm):
    
    file = forms.FileField(
        required=False, 
        widget=forms.ClearableFileInput(attrs={
            'multiple': False, 
            'class': 'form-control', 
            'id': 'taskFiles'
        })
    )
    do_up_to = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'id': 'taskDateTime'
        })
    )
    
    class Meta:
        model = Task
        exclude = ('course', 'has_quiz')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Назва завдання',
                'id': 'taskName'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Опис завдання',
                'id': 'taskDescription',
                'required': True
            }),
            'max_mark': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Максимальний бал',
                'min': '0',
                'id': 'taskMaxMark'
            })
        }
        
    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        
        if cleaned_data['do_up_to'] and timezone.now() > cleaned_data['do_up_to']:
            errors = self._errors.setdefault('do_up_to', ErrorList())
            errors.append('Некоретні дата та/або час')
            raise forms.ValidationError('Некоретні дата та/або час')
