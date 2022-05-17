from django.shortcuts import render
from django.views import View

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
    
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, self.template_name)
        
        context = {
            'created_courses': Course.objects.filter(owner=request.user),
            'joined_courses': []
        }
        user_courses = UserCourse.objects.filter(user=request.user)
        
        for user_course in user_courses:
            context['joined_courses'].append(user_course.course)

        return render(request, self.template_name, context)
