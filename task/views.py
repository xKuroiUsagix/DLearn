from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views import View
from django.http.response import HttpResponseForbidden

from course.models import Course, UserCourse
from dlearn.settings import MEDIA_ROOT
from quiz.models import Quiz
from .models import Task, UserTask, OwnerTaskFile, UserTaskFile
from .forms import TaskForm


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
        type form: TaskForm
    """
    model = Task
    form = TaskForm
    template_name = 'task/create.html'
    
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        if course.owner != request.user:
            return HttpResponseForbidden()
        
        context = {
            'course': course,
            'form': self.form,
            'my_courses': UserCourse.objects.filter(user=request.user),
            'created_courses': Course.objects.filter(owner=request.user)
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
        owner_files = OwnerTaskFile.objects.filter(task=task)
        
        try:
            quiz = Quiz.objects.get(task=task.id)
        except ObjectDoesNotExist:
            quiz = None
        
        context = {
            'course_id': course_id,
            'task': task,
            'quiz': quiz,
            'is_owner': task.course.owner == request.user,
            'files': owner_files,
            'my_courses': UserCourse.objects.filter(user=request.user),
            'created_courses': Course.objects.filter(owner=request.user)
        }
        return render(request, self.tempalte_name, context)

    def post(self, request, course_id, task_id):
        task = get_object_or_404(self.model, id=task_id)
        
        if task.has_quiz:
            quiz = Quiz.objects.get(task=task)
            quiz.delete()
        
        return redirect(f'/course/{course_id}/task/{task_id}/')

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
        task = get_object_or_404(self.model, id=task_id)
        task.delete()
        return redirect(f'/course/{course_id}/')


class TaskUpdateView(View):
    
    model = Task
    template_name = 'task/edit.html'
    form = TaskForm
    
    def get(self, request, course_id, task_id):
        task = get_object_or_404(self.model, id=task_id)
        form = self.form(instance=task)
        return render(request, self.template_name, {'form': form})

    def post(self, request, course_id, task_id):
        task = get_object_or_404(self.model, id=task_id)
        form = self.form(request.POST, request.FILES)
        owner_task_file = OwnerTaskFile.objects.filter(owner=request.user, task=task)
        
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        
        if task.name != form.cleaned_data['name']:
            task.name = form.cleaned_data['name']
        if task.description != form.cleaned_data['description']:
            task.description = form.cleaned_data['description']
        if task.mark != form.cleaned_data['mark']:
            task.mark = form.cleaned_data['mark']
        if task.do_up_to != form.cleaned_data['do_up_to']:
            task.do_up_to = form.cleaned_data['do_up_to']
        
        previous_media = [record.media for record in owner_task_file]
        for file in request.FILES.getlist('file'):
            if file not in previous_media:
                new_record = OwnerTaskFile()
                new_record.task = task
                new_record.owner = request.user
                new_record.media = file
        
        for record in owner_task_file:
            if record.media not in request.FILES.getlist('file'):
                record.delete()


class DeleteOwnerFileView(View):
    
    model = OwnerTaskFile
    
    def post(self, request, course_id, task_id, file_id):
        owner_file = self.model.objects.get(id=file_id)
        if owner_file.owner != request.user:
            return HttpResponseForbidden()
        
        owner_file.delete()
        return redirect(f'/course/{course_id}/task/{task_id}/')


class TaskDoneView(View):
    
    model = UserTask
    
    def post(self, request, course_id, task_id):
        task = get_object_or_404(Task, id=task_id)
        
        try:
            user_task = UserTask.objects.get(task=task, user=request.user)
        except ObjectDoesNotExist:
            user_task = UserTask()
            user_task.task = task
            user_task.user = request.user
            user_task.save()
        
        for file in request.FILES.getlist('file'):
            user_files = UserTaskFile()
            user_files.media = file
            user_files.user = request.user
            user_files.task = task
            user_files.save()
        
        return redirect(f'/course/{course_id}/task/{task_id}/')         
