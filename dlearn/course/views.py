from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import (
    FormView,
    UpdateView,
    DetailView,
    ListView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.core.exceptions import ObjectDoesNotExist

from authentication.errors import ErrorMessages
from task.models import Task, UserTask
from quiz.models import Quiz, UserResult

from .models import Course, UserCourse
from .forms import CourseCreateForm, CourseJoinForm, CourseUpdateForm


User = auth.get_user_model()


class CourseCreateView(LoginRequiredMixin, FormView):
    """
    A view for displaying CourseCreateForm for authenticated users
    and rendering a template response.
    """
    template_name = 'course/create.html'
    form_class = CourseCreateForm

    def form_valid(self, form):
        course = form.save(commit=False)
        course.owner = self.request.user
        course.image = self.request.FILES.get('image')
        course.save()
        
        return HttpResponseRedirect(f'/course/{course.id}/')


class CourseJoinView(LoginRequiredMixin, FormView):
    """
    A view for displaying CourseJoinForm for authenticated users
    and rendering a template response.
    """
    template_name = 'homepage/index.html'
    form_class = CourseJoinForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        try:
            self.course = Course.objects.get(join_code=form.data['join_code'])
        except ObjectDoesNotExist:
            self.course = None
        
        if self.is_form_valid(form):
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        user_course = UserCourse()
        user_course.user = self.request.user
        user_course.course = self.course
        user_course.save()
        return HttpResponseRedirect(f'/course/{self.course.id}')
    
    def form_invalid(self, form):
        context_data = self.get_context_data(form=form, join_error=True, join_open=True)
        return self.render_to_response(context_data)
    
    def is_form_valid(self, form):
        error_messages = []
        
        if not self.course or not self.course.check_password(form.data['password']):
            error_messages.append(ErrorMessages.BAD_PASSWORD_OR_JOINCODE_ERROR)
        if UserCourse.objects.filter(user=self.request.user, course=self.course):
            error_messages.append(ErrorMessages.USER_ALREADY_JOINED_ERROR)
        if self.course and self.course.owner == self.request.user:
            error_messages.append(ErrorMessages.USER_IS_OWNER_ERROR)
        
        if error_messages:
            form.errors['join_code'] = form.error_class(error_messages)
            return False
        return True
    
    def get_context_data(self, **kwargs):
        context_data = super(CourseJoinView, self).get_context_data(**kwargs)
        context_data['join_form'] = context_data.get('form')
        context_data['join_open'] = True
        return context_data


class CourseDetailView(LoginRequiredMixin, DetailView):
    """
    A view for rendering course detail template for authenticated users.
    """
    template_name = 'course/detail.html'
    pk_url_kwarg = 'course_id'
    model = Course
    
    def get_context_data(self, **kwargs):
        context_data = super(CourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object(queryset=self.model.objects.select_related('owner'))
        context_data['tasks'] = Task.objects.filter(course=course)
        context_data['is_owner'] = course.owner == self.request.user
        return context_data


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    A view for course deletion for authenticated user
    if the last one is an owner of this course and rendering
    a template response.
    """
    success_url = '/'
    model = Course
    
    def post(self, request, course_id):
        self.model.objects.get(id=course_id).delete()
        return HttpResponseRedirect(self.success_url)

    def test_func(self):
        return bool(self.request.POST.get('is_owner'))


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view for displaying CourseUpdateForm for authenticated users
    if the last one is an owner of this course. 
    """
    template_name = 'course/settings.html'
    pk_url_kwarg = 'course_id'
    model = Course
    form_class = CourseUpdateForm
    
    def form_valid(self, form):
        course = self.get_object()
        
        if form.data['name'] != course.name:
            course.name = form.data['name']
        if form.data.get('new_password'):
            course.set_password(form.data.get('new_password'))
        if form.data['join_code'] != course.join_code:
            course.join_code = form.data['join_code']
        if form.data['group_name'] != course.group_name:
            course.group_name = form.data['group_name']
        if form.data['password']:
            course.set_password(form.data['password'])
        if self.request.FILES.get('image'):
            course.image = self.request.FILES.get('image')
        
        course.save()
        return HttpResponseRedirect(f'/course/{course.id}/')
    
    def test_func(self):
        return self.get_object().owner == self.request.user


class UserCourseView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    A view for rendering course users template for authenticated users
    if the last one is an owner of this course.
    """
    model = UserCourse
    pk_url_kwarg = 'course_id'
    context_object_name = 'users_course'
    template_name = 'course/course_users.html'

    def __init__(self, **kwargs) -> None:
        super(UserCourseView, self).__init__(**kwargs)
        self.course = None
    
    def get_queryset(self):
        if self.queryset:
            return self.queryset
        
        self.queryset = self.get_course_object().users.all()
        return self.queryset
    
    def get_course_object(self):
        if self.course:
            return self.course
        
        self.course = get_object_or_404(Course, id=self.kwargs.get(self.pk_url_kwarg))
        return self.course
    
    def get_context_data(self, **kwargs):
        context_data = super(UserCourseView, self).get_context_data(**kwargs)
        course_tasks = Task.objects.select_related('course').filter(course=self.course)
        context_data['course'] = self.course
        context_data['tasks'] = course_tasks
        context_data['users_marks'] = self.get_users_marks(course_tasks)
        return context_data
    
    def get_users_marks(self, course_tasks):
        users_marks = {}
        task_quiz = {}
        
        for user in self.queryset:
            users_marks[user] = []
        
        for task in course_tasks:
            try:
                task_quiz[task] = Quiz.objects.get(task=task)
            except ObjectDoesNotExist:
                task_quiz[task] = '-'
        
        for user in users_marks.keys():
            for task, quiz in task_quiz.items():
                try:
                    users_marks.append(
                        UserTask.objects.get(user=user, task=task)
                    )
                except ObjectDoesNotExist:
                    users_marks.append('-')
                
                if quiz == '-':
                    users_marks.append('-')
                else:
                    try:
                        users_marks[user].append (
                            UserResult.objects.get(user=user, quiz=quiz).mark
                        )
                    except ObjectDoesNotExist:
                        users_marks.append('-')
        
        return users_marks
    
    def test_func(self):
        return self.get_course_object().owner == self.request.user


class KickUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    A view for kicking users from a course for authenticated users
    if the last one is an onwer of this course.
    """
    model = UserCourse
    course = None
    course_url_kwarg = 'course_id'
    
    def post(self, request, course_id, user_id):
        course = get_object_or_404(Course, id=course_id)
        user = get_object_or_404(User, id=user_id)
        user_course = get_object_or_404(self.model, course=course, user=user)
        user_course.delete()
        return HttpResponseRedirect(f'/course/{course.id}/users/')

    def get_course_object(self):
        if self.course:
            return self.course
        self.course = get_object_or_404(Course, id=self.kwargs.get(self.course_url_kwarg))
        return self.course
        
    def test_func(self):
        return self.get_course_object().owner == self.request.user
 
class LeaveCourseView(LoginRequiredMixin, View):
    """
    A view for leaving a course for authenticated users.
    """
    model = UserCourse
    success_url = '/'
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user_course = get_object_or_404(self.model, user=request.user, course=course)
        user_course.delete()
        return HttpResponseRedirect(self.success_url)
