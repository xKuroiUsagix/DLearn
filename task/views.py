from django.shortcuts import redirect, render
from django.views import View

from course.models import Course
from .models import Task
from .forms import TaskCreateForm


class TaskCreateView(View):
    
    model = Task
    form = TaskCreateForm
    template_name = 'task/create.html'
    
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        context = {
            'course': course,
            'form': self.form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, course_id, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        course = form.data['course']
        context = {
            'course': course,
            'form': form
        }
        
        if form.is_valid():
            form.save()
            return redirect(f'/')
        
        return render(request, self.template_name, context)
        
        
