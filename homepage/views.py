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
        context = {
            'my_courses': UserCourse.objects.filter(user=request.user),
            'created_courses': Course.objects.filter(owner=request.user)
        }
        return render(request, self.template_name, context)
