from django.forms import ModelForm
from django import forms

from .models import CustomUser


class RegistrationForm(ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'patronymic',
        ]
        
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('password and confirm password don\'t mathc')
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user


class LoginForm(ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    
    class Meta:
        model = CustomUser
        fields = ['email']
