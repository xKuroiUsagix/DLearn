from django.shortcuts import render
from django.views import View
from authentication.forms import LoginForm

from course.models import UserCourse, Course


class IndexView(View):
    """
        IndexView render the home page.
        
        Attributes:
        ----------
        param template_name: Describes template name for render
        type template_name: str
    """
    template_name = 'homepage/index.html'
    form = LoginForm
    
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, self.template_name, {'form': self.form})
        
        context = {
            'created_courses': Course.objects.filter(owner=request.user),
            'joined_courses': []
        }
        user_courses = UserCourse.objects.filter(user=request.user)
        
        for user_course in user_courses:
            context['joined_courses'].append(user_course.course)

        return render(request, self.template_name, context)
