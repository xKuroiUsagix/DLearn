from django import forms
from django.utils.translation import gettext_lazy as _

from authentication.validators import is_password_valid
from authentication.errors import ErrorMessages
from .models import Course


class CourseCreateForm(forms.ModelForm):
    
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'назва'}))
    password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'пароль'}))
    confirm_password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'повторіть пароль'}))
    group_name = forms.CharField(max_length=60, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'група'}))
    join_code = forms.CharField(max_length=20, min_length=5, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'код долучення'}))
    
    class Meta:
        model = Course
        fields = [
            'name',
            'group_name',
            'join_code',
        ]
        
    def clean(self):
        """Redefined clean method to validate password and cofirm_password

        Raises:
            forms.ValidationError: 
                - raise if password and confirm password don't match
                - raise of password doesn't contain at least 1 character and at least 1 number
        """
        cleaned_data = super(CourseCreateForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if not is_password_valid(password):
            raise forms.ValidationError(ErrorMessages.PASSWORD_VALIDATION_ERROR)
        if password != confirm_password:
            raise forms.ValidationError(ErrorMessages.PASSWORD_NOT_MATCH_ERROR)
        
    def save(self, commit=True):
        """Redefined save method to set hashed course password

        Args:
            commit (bool, optional): Saves the model if commit=True. Defaults to True.

        Returns:
            Course: The new created course
        """
        course = super(CourseCreateForm, self).save(commit=False)
        course.set_password(self.cleaned_data['password'])
        
        if commit:
            course.save()
        return course


class CourseJoinForm(forms.ModelForm):
    
    password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'пароль'}))
    
    class Meta:
        model = Course
        fields = [
            'join_code',
            'password'
        ]
        widgets = {
            'join_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'код долучення'})
        }


class CourseUpdateForm(forms.ModelForm):
    
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'пароль'}))
    new_password = forms.CharField(min_length=6, max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'новий пароль'}))
    confirm_password = forms.CharField(min_length=6, max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'повторіть пароль'}))
    
    class Meta:
        model = Course
        fields = [
            'name',
            'group_name',
            'join_code',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'назва'}),
            'group_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'група'}),
            'join_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'код долучення'})
        }
    
    def clean(self):
        cleaned_data = super(CourseUpdateForm, self).clean()

        if not self.instance.check_password(cleaned_data['password']):
            raise forms.ValidationError(ErrorMessages.BAD_PASSWORD_ERROR)
        if cleaned_data['new_password'] and cleaned_data['new_password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError(ErrorMessages.PASSWORD_NOT_MATCH_ERROR)
        if cleaned_data['new_password'] and not is_password_valid(cleaned_data['new_password']):
            raise forms.ValidationError(ErrorMessages.PASSWORD_VALIDATION_ERROR)
