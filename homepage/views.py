from django.shortcuts import render
from django.views import View

from .side_functions import context_add_courses


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
        context = {}
        
        if request.user.is_authenticated:
            context = context_add_courses(context, request.user)

        return render(request, self.template_name, context)
