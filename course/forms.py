from django import forms
from django.utils.translation import gettext_lazy as _

from authentication.validators import is_password_valid
from .models import Course, UserCourse


class CourseCreateForm(forms.ModelForm):
    
    name = forms.CharField(max_length=128, widget=forms.TextInput())
    password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput())
    confrim_password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput())
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
        """Redefined clean method to validate password and cofirm_password

        Raises:
            forms.ValidationError: 
                - raise if password and confirm password don't match
                - raise of password doesn't contain at least 1 character and at least 1 number
        """
        cleaned_data = super(CourseCreateForm, self).clean()
        password = cleaned_data.get('password')
        confrim_password = cleaned_data.get('confrim_password')

        if not is_password_valid(password):
            raise forms.ValidationError(_('Passwrod should contains at least 1 character, at least 1 number'))
        if password != confrim_password:
            raise forms.ValidationError(_('Password and confirm password don\'t match'))
        
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
    
    password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput())
    
    class Meta:
        model = Course
        fields = [
            'join_code',
            'password'
        ]
    
    def __init__(self, user, *args, **kwargs):
        """Redefined ModelForm constructor to set the user instance in the form

        Args:
            user (CustomUser): The user that want to join to the course
        """
        self.user = user
        super(CourseJoinForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        """Redefined clean method to set few custom validations

        Raises:
            forms.ValidationError:
                - raise when there is no course with given join_code or wrong password
                - raise when the user have already joined this course
                - raise when the user is the owner of this course
        """
        cleaned_data = super(CourseJoinForm, self).clean()
        self._validate_unique = False
        course = Course.objects.get(join_code=cleaned_data['join_code'])
        
        if not course or not course.check_password(cleaned_data['password']):
            raise forms.ValidationError(_('Bad course Join Code or Password'))
        if UserCourse.objects.filter(user=self.user, course=course):
            raise forms.ValidationError(_('You have already joined this course.'))
        if Course.objects.filter(owner=self.user):
            raise forms.ValidationError(_('You are the owner of this course'))
    
    def save(self, commit=True):
        """Redefined save method to join user to the course in the UserCourse model

        Args:
            commit (bool, optional): Saves the model if commit=True. Defaults to True.

        Returns:
            UserCourse: object of the UserCourse model
        """
        user_course = UserCourse()
        user_course.user = self.user
        user_course.course = self.cleaned_data.get('course')
        
        if commit:
            user_course.save()
        return user_course
