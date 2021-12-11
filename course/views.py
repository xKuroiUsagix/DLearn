from django.shortcuts import redirect, render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .models import Course, UserCourse
from .forms import CourseCreateForm, CourseJoinForm


class CourseCreateView(View):
    
    model = Course
    template_name = 'course/create.html'
    form = CourseCreateForm
    
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/auth/login')
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        
        if not request.user.is_authenticated:
            return redirect('/auth/login')
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            return redirect(f'/profile/{request.user.id}/owned-courses')
        return render(request, self.template_name, {'form': form})


class CourseJoinView(View):
    
    model = Course
    template_name = 'course/join.html'
    form = CourseJoinForm
    
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/auth/login')
        return render(request, self.template_name, {'form': self.form})
    
    def post(self, request):
        form = self.form(request.POST)
        
        try:
            course = Course.objects.get(join_code=form.data['join_code'])
        except ObjectDoesNotExist:
            course = None
        
        if not course or not course.check_password(form.data['password']):
            form.errors['join_code'] = form.error_class([_('Bad course Join Code or Password')])
            return render(request, self.template_name, {'form': form})
        if UserCourse.objects.filter(user=request.user, course=course):
            form.errors['join_code'] = form.error_class([_('You have already joined this course.')])
            return render(request, self.template_name, {'form': form})
        if Course.objects.filter(owner=request.user):
            form.errors['join_code'] = form.error_class([_('You are the owner of this course')])
            return render(request, self.template_name, {'form': form})
        
        user_course = UserCourse()
        user_course.user = request.user
        user_course.course = course
        user_course.save()
        
        return redirect(f'/profile/{request.user.id}/joined-courses')
