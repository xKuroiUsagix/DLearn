from django.shortcuts import redirect, render
from django.views import View
from django.http.response import HttpResponseForbidden

from course.models import Course
from .models import Task, OwnerTaskFile
from .forms import TaskCreateForm


class TaskCreateView(View):
    
    model = Task
    form = TaskCreateForm
    template_name = 'task/create.html'
    
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        if course.owner != request.user:
            return HttpResponseForbidden()
        
        context = {
            'course': course,
            'form': self.form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, course_id, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        course = Course.objects.get(id=course_id)
        context = {
            'course': course,
            'form': form
        }
        
        if form.is_valid():
            task = form.save(commit=False)
            task.course = course
            task.save()
            
            for file in request.FILES.getlist('file'):
                owner_task_file = OwnerTaskFile()
                owner_task_file.owner = request.user
                owner_task_file.task = task
                owner_task_file.media = file
                owner_task_file.save()
            
            return redirect(f'/course/{course.id}/')
        
        return render(request, self.template_name, context)


class TaskDetailView(View):
    
    model = Task
    tempalte_name = 'task/detail.html'
    
    def get(self, request, course_id, task_id):
        task = self.model.objects.get(id=task_id)
        return render(request, self.tempalte_name, {'task': task})


class TaskDeleteView(View):
    
    model = Task
    
    def post(self, request, course_id, task_id):
        self.model.objects.get(id=task_id).delete()
        return redirect(f'/course/{course_id}/')
