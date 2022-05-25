from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

from authentication.validators import is_password_valid
from authentication.errors import ErrorMessages
from .models import Course


class CourseCreateForm(forms.ModelForm):
    
    confirm_password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторіть Пароль'}))
    
    class Meta:
        model = Course
        fields = [
            'name',
            'password',
            'group_name',
            'join_code',
            'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control course-form-input',
                'placeholder': 'Назва Курсу',
                'maxlength': '128'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'minlength': '6',
                'maxlength': '20'
            }),
            'group_name': forms.TextInput(attrs={
                'class': 'form-control course-form-input',
                'placeholder': 'Група',
                'maxlength': '60',
            }),
            'join_code': forms.TextInput(attrs={
                'class': 'form-control course-form-input',
                'placeholder': 'Код Долучення',
                'minlength': '5',
                'maxlength': '20',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Зображення Курсу',
            })
        }
        
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
            errors = self._errors.setdefault('password', ErrorList())
            errors.append(ErrorMessages.PASSWORD_NOT_MATCH_ERROR)
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


class CourseUpdateForm(forms.ModelForm):
    
    password = forms.CharField(required=False,
                               min_length=6,
                               max_length=20,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control course-form-input',
                                   'placeholder': 'Новий пароль'
                               }))
    confirm_password = forms.CharField( min_length=6, 
                                        max_length=20, 
                                        required=False, 
                                        widget=forms.PasswordInput(attrs={
                                            'class': 'form-control course-form-input', 
                                            'placeholder': 'Повторіть пароль'
                                        }))
    
    class Meta:
        model = Course
        fields = [
            'name',
            'group_name',
            'join_code',
            'image',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control course-form-input',
                'placeholder': 'Назва Курсу',
                'maxlength': '128'
            }),
            'group_name': forms.TextInput(attrs={
                'class': 'form-control course-form-input',
                'placeholder': 'Група',
                'maxlength': '60',
            }),
            'join_code': forms.TextInput(attrs={
                'class': 'form-control course-form-input',
                'placeholder': 'Код Долучення',
                'minlength': '5',
                'maxlength': '20',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Зображення Курсу',
            })
        }
    
    def clean(self):
        cleaned_data = super(CourseUpdateForm, self).clean()

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            errors = self._errors.setdefault('password', ErrorList())
            errors.append(ErrorMessages.PASSWORD_NOT_MATCH_ERROR)
            raise forms.ValidationError(ErrorMessages.PASSWORD_NOT_MATCH_ERROR)
        if not is_password_valid(cleaned_data['password']):
            errors = self._errors.setdefault('password', ErrorList())
            errors.append(ErrorMessages.PASSWORD_VALIDATION_ERROR)
            raise forms.ValidationError(ErrorMessages.PASSWORD_VALIDATION_ERROR)


class CourseJoinForm(forms.ModelForm):
    
    class Meta:
        model = Course
        fields = [
            'join_code',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Пароль Курсу'
            }),
            'join_code': forms.TextInput(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Код Долучення'
            })
        }
