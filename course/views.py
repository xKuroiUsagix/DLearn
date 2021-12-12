from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from authentication.errors import ErrorMessages
from .models import Course, UserCourse
from .forms import CourseCreateForm, CourseJoinForm, CourseUpdateForm


class CourseCreateView(View):
    
    model = Course
    template_name = 'course/create.html'
    form = CourseCreateForm
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            return redirect(f'/course/owned-courses')
        return render(request, self.template_name, {'form': form})


class CourseJoinView(View):
    
    model = Course
    template_name = 'course/join.html'
    form = CourseJoinForm
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})
    
    def post(self, request):
        form = self.form(request.POST)
        
        try:
            course = Course.objects.get(join_code=form.data['join_code'])
        except ObjectDoesNotExist:
            course = None
        
        if not course or not course.check_password(form.data['password']):
            form.errors['join_code'] = form.error_class([ErrorMessages.BAD_PASSWORD_OR_JOINCODE_ERROR])
            return render(request, self.template_name, {'form': form})
        if UserCourse.objects.filter(user=request.user, course=course):
            form.errors['join_code'] = form.error_class([ErrorMessages.USER_ALREADY_JOINED_ERROR])
            return render(request, self.template_name, {'form': form})
        if Course.objects.filter(owner=request.user):
            form.errors['join_code'] = form.error_class([ErrorMessages.USER_IS_OWNER_ERROR])
            return render(request, self.template_name, {'form': form})
        
        user_course = UserCourse()
        user_course.user = request.user
        user_course.course = course
        user_course.save()
        
        return redirect(f'/course/joined-courses/')


class OwnedCoursesView(View):
    
    model = Course
    template_name = 'course/owner-courses.html'

    def get(self, request):
        courses = self.model.objects.filter(owner=request.user)
        context = {
            'courses': courses
        }
        return render(request, self.template_name, context)


class JoinedCoursesView(View):
    
    model = UserCourse
    template_name = 'course/joined-courses.html'
    
    def get(self, request):
        user_courses = self.model.objects.filter(user=request.user)
        courses = []
        
        for item in user_courses:
            courses.append(item.course)
        
        context = {
            'courses': courses
        }
        
        return render(request, self.template_name, context)


class CourseDetailView(View):
    
    model = Course
    template_name = 'course/detail.html'
    
    def get(self, request, pk, *args, **kwargs):
        course = self.model.objects.get(id=pk)
        is_owner = True if course.owner == request.user else False
        
        context = {
            'course': course,
            'is_owner': is_owner
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        course = self.model.objects.get(id=pk)
        
        if course.owner != request.user and request.POST.get('delete'):
            return HttpResponseForbidden()
        
        if request.POST.get('leave'):
            user_course = UserCourse.objects.get(user=request.user, course=course)
            user_course.delete()
            return redirect('/course/joined-courses/')
        
        course.delete()
        return redirect('/course/owned-courses/')
        
        
class CourseUpdateView(View):
    
    model = Course
    form = CourseUpdateForm
    template_name = 'course/settings.html'
    
    def get(self, request, pk, *args, **kwargs):
        course = self.model.objects.get(id=pk)
        context = {
            'course': course,
            'form': self.form(instance=course)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        course = self.model.objects.get(id=pk)
        form = self.form(request.POST, instance=course)
        context = {
            'course': course,
            'form': form
        }
        
        if not form.is_valid():
            return render(request, self.template_name, context)
        
        if form.data['name'] != course.name:
            course.name = form.data['name']
        if form.data['new_password']:
            course.set_password(form.data['new_password'])
        if form.data['join_code'] != course.join_code:
            course.join_code = form.data['join_code']
        if form.data['group_name'] != course.group_name:
            course.group_name = form.data['group_name']
        
        course.save()
        return redirect(f'/course/{course.id}/')
