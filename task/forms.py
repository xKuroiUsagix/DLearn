from django import forms
from django.forms.utils import ErrorList
from django.utils import timezone
from django.forms import widgets

from datetime import datetime

from .models import Task


class TaskForm(forms.ModelForm):
    
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))
    do_up_to = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Task
        exclude = ('course', 'has_quiz')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'назва'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'опис завдання'}),
            'max_mark': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'максимальний бал'})
        }
        
    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        
        if cleaned_data['do_up_to'] and timezone.now() > cleaned_data['do_up_to']:
            errors = self._errors.setdefault('do_up_to', ErrorList())
            errors.append('Дата та час мають бути в майбутньому')
            raise forms.ValidationError('Дата та час мають бути в майбутньому')
