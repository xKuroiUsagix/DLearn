from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views import View
from django.http.response import HttpResponseForbidden

from course.models import Course, UserCourse
from dlearn.settings import MEDIA_ROOT
from quiz.models import Quiz
from homepage.side_functions import context_add_courses
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
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.template_name, context)
    
    def post(self, request, course_id):
        form = self.form(request.POST, request.FILES)
        course = get_object_or_404(Course, id=course_id)
        context = {
            'course': course,
            'form': form
        }
        context = context_add_courses(context, request.user)
        
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
        If the user is owner of the course - he has additional functions.
        
        Abilities for owner:
            - Delete task
            - Modify task
            - Delete included files
        
        Abilities for joined user:
            - See the task
            - Add files to the task
        
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
        user_files = UserTaskFile.objects.filter(task=task)
        
        try:
            quiz = Quiz.objects.get(task=task)
        except ObjectDoesNotExist:
            quiz = None
        
        context = {
            'course_id': course_id,
            'task': task,
            'quiz': quiz,
            'is_owner': task.course.owner == request.user,
            'owner_files': owner_files,
            'user_files': user_files
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.tempalte_name, context)

    def post(self, request, course_id, task_id):
        task = get_object_or_404(self.model, id=task_id)
        
        try:
            Quiz.objects.get(task=task).delete()
        except ObjectDoesNotExist:
            pass
        
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
    """
        TaskUpdateView provides operations for course owner to update task info.
        
        Attributes:
        ----------
        param model: Describes the Task model in database
        type model: Task
        param template_name: Describes template name for render
        type template_name: str
        param form: Describes the form for Task
        type form: TaskForm
    """
    
    model = Task
    template_name = 'task/edit.html'
    form = TaskForm
    
    def get(self, request, course_id, task_id):
        task = get_object_or_404(self.model, id=task_id)
        form = self.form(instance=task)
        owner_files = OwnerTaskFile.objects.filter(task=task)
        
        context = {
            'form': form,
            'course_id': course_id,
            'task_id': task_id,
            'files': owner_files
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.template_name, context)

    def post(self, request, course_id, task_id):
        task = get_object_or_404(self.model, id=task_id)
        form = self.form(request.POST, request.FILES)
        owner_task_file = OwnerTaskFile.objects.filter(owner=request.user, task=task)
        context = {
            'form': form
        }
        context = context_add_courses(context, request.user)
        
        if not form.is_valid():
            return render(request, self.template_name, context)
        
        if task.name != form.cleaned_data['name']:
            task.name = form.cleaned_data['name']
        if task.description != form.cleaned_data['description']:
            task.description = form.cleaned_data['description']
        if task.do_up_to != form.cleaned_data['do_up_to']:
            task.do_up_to = form.cleaned_data['do_up_to']
        task.save()
        
        previous_media = [record.media for record in owner_task_file]
        for file in request.FILES.getlist('file'):
            if file not in previous_media:
                new_record = OwnerTaskFile()
                new_record.task = task
                new_record.owner = request.user
                new_record.media = file
                new_record.save()
        
        return redirect(f'/course/{course_id}/task/{task_id}/')


class DeleteOwnerFileView(View):
    """
        DeleteOwnerfileView provides operations for course owner to delete included files.
        
        Attributes:
        ----------
        param model: Describes the OwnerTaskFile model in database
        type model: OwnerTaskFile
    """
    
    model = OwnerTaskFile
    
    def post(self, request, course_id, task_id, file_id):
        owner_file = self.model.objects.get(id=file_id)
        if owner_file.owner != request.user:
            return HttpResponseForbidden()
        
        owner_file.delete()
        return redirect(f'/course/{course_id}/task/{task_id}/')


class DeleteUserFileView(View):
    """
        DeleteUserFileView provides operations for course user to delete his included files.
        
        Attributes:
        ----------
        param model: Describes the UserTaskFile model in database
        type model: UserTaskFile
    """
    model = UserTaskFile
    
    def post(self, request, course_id, task_id, file_id):
        user_file = self.model.objects.get(id=file_id);
        if user_file.user != request.user:
            return HttpResponseForbidden()
        
        user_file.delete()
        return redirect(f'/course/{course_id}/task/{task_id}/')


class AddUserFilesView(View):
    """
        AddUserFilesview provides operations for course user to add files as answer.
        
        Attributes:
        ----------
        param model: Describes the UserTaskFile model in database
        type model: UserTaskFile
    """
    model = UserTaskFile
    
    def post(self, request, course_id, task_id):
        task = get_object_or_404(Task, id=task_id)
        user_task_files = self.model.objects.filter(task=task, user=request.user)
            
        previous_media = [record.media for record in user_task_files]
        for file in request.FILES.getlist('file'):
            if file not in previous_media:
                self.model.objects.create(
                    media=file,
                    user=request.user,
                    task=task
                )
        
        return redirect(f'/course/{course_id}/task/{task_id}/')         


class UserFilesListView(View):
    """
        UserFilesListView provides operations for course owner to see all user files for this task.
        
        Attributes:
        ----------
        param model: Describes the UserTaskFile model in database
        type model: UserTaskFile
        param template_name: Describes template name for render
        type template_name: str
    """
    model = UserTaskFile
    tenplate_name = 'task/user-files.html'
    
    def get(self, request, course_id, task_id):
        task = get_object_or_404(Task, id=task_id)
        user_task_files = self.model.objects.filter(task=task)
        user_files = {}
        
        for user_task_file in user_task_files:
            user = f'{user_task_file.user.first_name} {user_task_file.user.last_name}'
            
            if user in user_files.keys():
                user_files[user].append(user_task_file)
            else:
                user_files[user] = [user_task_file]
        
        context = {
            'user_files': user_files
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.tenplate_name, context)
