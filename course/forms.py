from django import forms

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
        cleaned_data = super(CourseCreateForm, self).clean()
        password = cleaned_data.get('password')
        confrim_password = cleaned_data.get('confrim_password')

        if not is_password_valid(password):
            raise forms.ValidationError('passwrod should contains at least 1 character, at least 1 number')
        if password != confrim_password:
            raise forms.ValidationError('password and confirm password don\'t match')
        
    def save(self, commit=True):
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
        self.user = user
        super(CourseJoinForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(CourseJoinForm, self).clean()
        self._validate_unique = False
        course = Course.objects.get(join_code=cleaned_data['join_code'])
        
        if not course:
            raise forms.ValidationError('No courses with thid Join Code')
        if UserCourse.objects.filter(user=self.user, course=course):
            raise forms.ValidationError('You have already joined this course.')
        if not course.check_password(cleaned_data['password']):
            raise forms.ValidationError('Wrong password')
    
    def save(self, commit=True):
        user_course = UserCourse()
        user_course.user = self.user
        user_course.course =  self.cleaned_data.get('course')
        
        if commit:
            user_course.save()
        return user_course
