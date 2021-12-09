from django.shortcuts import redirect, render
from django.views import View

from .models import Course
from .forms import CourseForm


class CreateCourseView(View):
    model = Course
    template_name = 'course/create.html'
    form = CourseForm
    
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
