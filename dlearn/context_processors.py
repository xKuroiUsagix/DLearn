from course.models import Course, UserCourse
from course.forms import CourseJoinForm

from authentication.forms import LoginForm


def add_courses_to_context(request):
    if not request.user.is_authenticated:
        return {
            'login_form': LoginForm
        }
    
    user_courses = UserCourse.objects.filter(user=request.user)
    added_courses = [user_course.course for user_course in user_courses]
    
    return {
        'created_courses': Course.objects.filter(owner=request.user),
        'added_courses': added_courses,
        'join_form': CourseJoinForm
    }
