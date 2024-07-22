from django.contrib import auth

from course.models import Course
from course.forms import CourseJoinForm
from authentication.forms import LoginForm


User = auth.get_user_model()


def add_courses_to_context(request):
    if not request.user.is_authenticated:
        return {
            'login_form': LoginForm
        }
    
    return {
        'created_courses': Course.objects.filter(owner=request.user).select_related('owner'),
        'joined_courses': request.user.courses.all(),
        'join_form': CourseJoinForm
    }
