from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from .models import CustomUser
from .froms import RegistrationForm


class RegisterView(View):
    template_name = 'authentication/register.html'
    form = RegistrationForm
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, self.template_name, {'form': form})
    