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
    
    def get(self, request):
        return render(request, self.template_name)
