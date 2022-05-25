from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from authentication.errors import ErrorMessages
from authentication.models import CustomUser
from task.models import Task
from .models import Course, UserCourse
from .forms import CourseCreateForm, CourseJoinForm, CourseUpdateForm


class CourseCreateView(View):
    """
        CourseCreateView provides operations for user to create own courses.
        
        Attributes:
        ----------
        param template_name: Describes template name for render
        type template_name: str
        param form: Describes django-form for course creation
        type form: CourseCreateForm
    """
    template_name = 'course/create.html'
    form = CourseCreateForm
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.image = request.FILES.get('image')
            course.save()
            return redirect(f'/course/{course.id}/')
        
        return render(request, self.template_name, {'form': form})


class CourseJoinView(View):
    """
        CourseJoinView provides operations for user to join courses.
        
        Attributes:
        ----------
        param model: Describes the Course model in database
        type model: Course
        param template_name: Describes template name for render
        type template_name: str
        param form: Describes django-form for course joining
        type form: CourseJoinForm
    """
    model = Course
    template_name = 'homepage/index.html'
    form = CourseJoinForm
    
    def get(self, request):
        return render(request, self.template_name, {'join_form': self.form})
    
    def post(self, request):
        form = self.form(request.POST)
        
        try:
            course = self.model.objects.get(join_code=form.data['join_code'])
            print(course.password)
        except ObjectDoesNotExist:
            course = None
        
        # This validation done here because of some troubles in doing...
        # this in the CourseJoinForm
        error_messages = []
        if not course or not course.check_password(form.data['password']):
            error_messages.append(ErrorMessages.BAD_PASSWORD_OR_JOINCODE_ERROR)
        if UserCourse.objects.filter(user=request.user, course=course):
            error_messages.append(ErrorMessages.USER_ALREADY_JOINED_ERROR)
        if course.owner == request.user:
            error_messages.append(ErrorMessages.USER_IS_OWNER_ERROR)
        
        if error_messages:
            form.errors['join_code'] = form.error_class(error_messages)
            return render(request, self.template_name, {'join_form': form, 'join_error': True})
        
        user_course = UserCourse()
        user_course.user = request.user
        user_course.course = course
        user_course.save()
        
        return redirect(f'/')


class CourseDetailView(View):
    """
        CourseDetailView provides operations for user to see course details.
        The details that user can see depends on user status in this course.
        If the user is owner of this course he will see some additional info in the template
        and also has ability to administrate his course.
        
        Abilities for owner:
            - Modify the course information
            - Delete the course
            - Create tasks for joined users
        
        Abilities for joined user:
            - Leave the course
            - See tasks created by owner
        
        Attributes:
        ----------
        param model: Describes the Course model in database
        type model: Course
        param template_name: Describes template name for render
        type template_name: str
    """
    model = Course
    template_name = 'course/detail.html'
    
    def get(self, request, pk):
        course = get_object_or_404(self.model, id=pk)
        tasks = Task.objects.filter(course=course)
        is_owner = course.owner == request.user
        user_course = UserCourse.objects.filter(course=course)
        joined_users = [record.user for record in user_course]
        
        context = {
            'tasks': tasks,
            'course': course,
            'is_owner': is_owner,
            'joined_users': joined_users
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        course = get_object_or_404(self.model, id=pk)
        
        if course.owner != request.user:
            return HttpResponseForbidden()
        
        course.delete()
        return redirect('/')
        
     
class CourseUpdateView(View):
    """
        CourseUpdateView provides operations for owner to change his course information.
        Owner can change every field in the course.
        
        Attributes:
        ----------
        param model: Describes the Course model in database
        type model: Course
        param template_name: Describes template name for render
        type template_name: str
        param form: Describes the form for updating course infromation
        type form: CourseUpdateForm
    """
    model = Course
    form = CourseUpdateForm
    template_name = 'course/settings.html'
    
    def get(self, request, pk):
        course = get_object_or_404(self.model, id=pk)
        context = {
            'course': course,
            'form': self.form(instance=course)
        }
            
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        course = get_object_or_404(self.model, id=pk)
        form = self.form(request.POST, instance=course)
        form.fields.get('password')
        context = {
            'course': course,
            'form': form
        }
        
        if not form.is_valid():
            return render(request, self.template_name, context)
        
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
        if request.FILES.get('image'):
            course.image = request.FILES.get('image')
        
        course.save()
        return redirect(f'/course/{course.id}/')


class UserCourseView(View):
    """
        UserCourseView provides operations for owner to see users joined to the course.
        Attributes:
        ----------
        param model: Describes the UserCourse model in database
        type model: UserCourse
    """
    model = UserCourse
    template_name = 'course/course_users.html'
    
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        context = {
            'course': course,
            'users_course': UserCourse.objects.filter(course=course)
        }
        
        return render(request, self.template_name, context)


class KickUserView(View):
    """
        KickUserView provides ability to kick users from course.
        Attributes:
        ----------
        param model: Describes the UserCourse model in database
        type model: UserCourse
    """
    model = UserCourse
    
    def post(self, request, course_id, user_id):
        course = get_object_or_404(Course, id=course_id)
        user = get_object_or_404(CustomUser, id=user_id)
        user_course = get_object_or_404(self.model, course=course, user=user)
        user_course.delete()
        return redirect(f'/course/{course.id}/users/')
 
class LeaveCourseView(View):
    """
        LeaveCourseView provides operations for the user to leave the course.
        
        Attributes:
        ----------
        param model: Describes the UserCourse model in database
        type model: UserCourse
    """
    model = UserCourse
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user_course = get_object_or_404(self.model, user=request.user, course=course)
        user_course.delete()
        return redirect('/')
