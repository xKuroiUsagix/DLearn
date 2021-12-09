from django import forms
from django.contrib.auth.hashers import make_password, check_password

from authentication.validators import is_password_valid
from .models import Course


class CourseForm(forms.ModelForm):
    
    name = forms.CharField(max_length=128, widget=forms.TextInput())
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    confrim_password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    group_name = forms.CharField(max_length=60, required=False, widget=forms.TextInput())
    join_code = forms.CharField(max_length=20, min_length=5, widget=forms.TextInput())
    
    class Meta:
        model = Course
        fields = [
            'name',
            'group_name',
            'join_code',
        ]
        
    def clean(self):
        cleaned_data = super(CourseForm, self).clean()
        join_code = cleaned_data.get('join_code')
        password = cleaned_data.get('password')
        confrim_password = cleaned_data.get('confrim_password')

        if not is_password_valid(password):
            raise forms.ValidationError('passwrod should contains at least 1 character, at least 1 number')
        if password != confrim_password:
            raise forms.ValidationError('password and confirm password don\'t match')
        
    def save(self, commit=True):
        course = super(CourseForm, self).save(commit=False)
        course.password = make_password(self.cleaned_data['password'])
        
        if commit:
            course.save()
        return course
