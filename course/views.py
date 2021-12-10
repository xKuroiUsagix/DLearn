from django.shortcuts import redirect, render
from django.views import View

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
        return render(request, self.template_name, {'form': self.form})
    
    def post(self, request):
        form = self.form(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{request.user.id}/joined-courses')
        return render(request, self.template_name, {'form': form})
