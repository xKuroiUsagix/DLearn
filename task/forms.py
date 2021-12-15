from django import forms
from django.forms import widgets

from .models import Task


class TaskCreateForm(forms.ModelForm):
    
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    do_up_to = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    
    class Meta:
        model = Task
        exclude = ('course',)
