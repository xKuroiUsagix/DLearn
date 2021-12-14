from django.utils.translation import gettext_lazy as _
from django import forms

from datetime import datetime

from .errors import ErrorMessages
from .models import CustomUser
from .validators import is_password_valid


BIRTH_DAY_CHOICES = [i+1 for i in range(31)]
BIRTH_YEAR_CHOICES = [i for i in range(1920, datetime.now().year)]
BIRTH_MONTH_CHOICES = [i+1 for i in range(12)]


def set_default_attrs(**kwargs):
    attrs = {'class': 'form-control'}
    for k, v in kwargs.items():
        attrs[k] = v
    return attrs


class RegistrationForm(forms.ModelForm):
    
    password = forms.CharField(min_length=6, max_length=30, widget=forms.PasswordInput(
        attrs=set_default_attrs(placeholder='Password')
    ))
    confirm_password = forms.CharField(min_length=6, max_length=30, widget=forms.PasswordInput(
        attrs=set_default_attrs(placeholder='Confirm Password')
    ))
    birthday = forms.DateField(widget=forms.SelectDateWidget(
        months=BIRTH_MONTH_CHOICES,
        years=BIRTH_YEAR_CHOICES,
    ))
    
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'birthday',
            'biology_sex'
        ]
        widgets = {
            'email': forms.EmailInput(attrs=set_default_attrs(placeholder='Email')),
            'first_name': forms.TextInput(attrs=set_default_attrs(placeholder='First Name')),
            'last_name': forms.TextInput(attrs=set_default_attrs(placeholder='Last Name')),
        }
        
    def clean(self):
        """Redefined method clean from ModelForm to add password confimation

        Raises:
            forms.ValidationError: 
                - raise if password and confirm password don't match
                - raise of password doesn't contain at least 1 character and at least 1 number
        """
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if not is_password_valid(password):
            raise forms.ValidationError(ErrorMessages.PASSWORD_VALIDATION_ERROR)
        if password != confirm_password:
            raise forms.ValidationError(ErrorMessages.PASSWORD_NOT_MATCH_ERROR)
    
    def save(self, commit=True):
        """Redefined method save from ModelForm

        Args:
            commit (bool, optional): 
            set to True in case to commit changes, set to False to get user object without commiting. Defaults to True.

        Returns:
            CustomUser: user object
        """
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    
    class Meta:
        model = CustomUser
        fields = ['email']
