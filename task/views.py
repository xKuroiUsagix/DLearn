from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views import View
from django.http.response import HttpResponseForbidden

from course.models import Course
from .models import Task, OwnerTaskFile
from .forms import TaskCreateForm


class TaskCreateView(View):
    """
        TaskCreateView provides operations for course owner to create tasks for his course.
        
        Attributes:
        ----------
        param model: Describes the Task model in database
        type model: Task
        param template_name: Describes template name for render
        type template_name: str
        param form: Describes the form for Task creation
        type form: TaskCreateForm
    """
    model = Task
    form = TaskCreateForm
    template_name = 'task/create.html'
    
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        if course.owner != request.user:
            return HttpResponseForbidden()
        
        context = {
            'course': course,
            'form': self.form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, course_id):
        form = self.form(request.POST, request.FILES)
        course = get_object_or_404(Course, id=course_id)
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
    """
        TaskDetailView provides operations for task detail information.
        If the user is owner of the course to which task belong to,
        than this user has additional abilities.
        
        Abilities for owner:
            - Delete task
            - Modify task
            - Set mark for each user that done this task
        
        Abilities for joined user:
            - See the task
            - Add files to the task
            - Note task as "done" 
        
        Attributes:
        ----------
        param model: Describes the Task model in database
        type model: Task
        param template_name: Describes template name for render
        type template_name: str
    """
    model = Task
    tempalte_name = 'task/detail.html'
    
    def get(self, request, course_id, task_id):
        task = get_object_or_404(self.model, id=task_id)
        return render(request, self.tempalte_name, {'task': task})


class TaskDeleteView(View):
    """
        TaskDeleteView provides ability to delete tasks for course owner.
        
        Attributes:
        ----------
        param model: Describes the Task model in database
        type model: Task
    """
    model = Task
    
    def post(self, request, course_id, task_id):
        task = get_object_or_404(self.mode, id=task_id)
        task.delete()
        return redirect(f'/course/{course_id}/')
