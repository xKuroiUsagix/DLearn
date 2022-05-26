from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views import View
from django.http.response import HttpResponseForbidden

from course.models import Course
from authentication.models import CustomUser
from dlearn.settings import MEDIA_ROOT
from quiz.models import Quiz, UserResult

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
            'task_form': self.form,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, course_id):
        form = self.form(request.POST, request.FILES)
        course = get_object_or_404(Course, id=course_id)
        context = {
            'course': course,
            'task_form': form
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
            user_task = UserTask.objects.get(task=task, user=request.user)
        except ObjectDoesNotExist:
            user_task = None
        
        try:
            quiz = Quiz.objects.get(task=task)
        except ObjectDoesNotExist:
            quiz = None
        
        context = {
            'course_id': course_id,
            'task': task,
            'quiz': quiz,
            'mark': user_task.mark if user_task else None,
            'is_examined': user_task.is_examined if user_task else None,
            'is_owner': task.course.owner == request.user,
            'owner_files': owner_files,
            'user_files': user_files
        }
        
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
            'task_form': form,
            'course_id': course_id,
            'task': task,
            'files': owner_files
        }
        
        return render(request, self.template_name, context)

    def post(self, request, course_id, task_id):
        task = get_object_or_404(self.model, id=task_id)
        form = self.form(request.POST, request.FILES)
        owner_files = OwnerTaskFile.objects.filter(task=task)
        context = {
            'course_id': course_id,
            'task': task,
            'files': owner_files,
        }

        if not form.is_valid():
            context['task_form'] = form
            return render(request, self.template_name, context)
        
        if task.name != form.cleaned_data['name']:
            task.name = form.cleaned_data['name']
        if task.description != form.cleaned_data['description']:
            task.description = form.cleaned_data['description']
        if task.max_mark != form.cleaned_data['max_mark']:
            task.max_mark = form.cleaned_data['max_mark']
        if form.cleaned_data['do_up_to']:
            task.do_up_to = form.cleaned_data['do_up_to']
        task.save()
        
        previous_media = [record.media for record in owner_files]
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
        
        task = Task.objects.get(id=task_id)
        user_task_files = UserTaskFile.objects.filter(user=request.user, task=task)
        if not user_task_files:
            UserTask.objects.get(user=request.user, task=task).delete()
        
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
        
        
        if UserTask.objects.filter(user=request.user, task=task):
            UserTask.objects.get(user=request.user, task=task).delete()
            
        UserTask.objects.create(
            task=task,
            user=request.user
        )
            
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
        if not Course.objects.get(id=course_id).owner == request.user:
            return HttpResponseForbidden()
        
        task = get_object_or_404(Task, id=task_id)
        users_task = UserTask.objects.filter(task=task)
        user_task_files = self.model.objects.filter(task=task)
        user_files = {}
        
        for user_task_file in user_task_files:
            if user_task_file.user in user_files.keys():
                user_files[user_task_file.user].append(user_task_file)
            else:
                user_files[user_task_file.user] = [user_task_file]
        
        context = {
            'task': task,
            'course_id': course_id,
            'users_task': users_task,
            'user_files': user_files
        }
        
        return render(request, self.tenplate_name, context)
    
    def post(self, request, course_id, task_id):
        if not Course.objects.get(id=course_id).owner == request.user:
            return HttpResponseForbidden()
        
        task = Task.objects.get(id=task_id)
        user = CustomUser.objects.get(id=int(request.POST.get('userID')))
        
        user_task = UserTask.objects.get(user=user, task=task)
        user_task.is_examined = True
        user_task.mark = int(request.POST.get('userMark'))
        user_task.save()
        
        return redirect(f'/course/{course_id}/task/{task_id}/user-files/')


class UserRatingView(View):
    template_name = 'task/users-rating.html'
    
    def get(self, request, course_id, task_id):
        task = Task.objects.get(id=task_id)
        users_task = UserTask.objects.filter(task=task)
        users_marks = {}
        
        try:
            quiz = Quiz.objects.get(task=task)
        except ObjectDoesNotExist:
            quiz = None
        
        if quiz:
            users_results = UserResult.objects.filter(quiz=quiz)
        
        for user_task in users_task:
            users_marks[user_task.user] = [user_task.mark]
        
        if quiz:
            for user_result in users_results:
                users_marks[user_result.user].append(user_result.mark)
        else:
            for user in users_marks:
                users_marks[user].append(0)
        
        for user, marks in users_marks.items():
            users_marks[user].append(sum(marks))    
        
        context = {
            'task_id': task_id,
            'course_id': course_id,
            'users_marks': users_marks
        }
        
        return render(request, self.template_name, context)
