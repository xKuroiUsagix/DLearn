from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from .models import CustomUser
from .froms import RegistrationForm, LoginForm


class RegisterView(View):
    template_name = 'authentication/register.html'
    form = RegistrationForm
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'form': form})
    

class LoginView(View):
    template_name = 'authentication/login.html'
    form = LoginForm
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})
    
    def post(self, request):
        form = self.form(request.POST)
        user = CustomUser.objects.get(email=form.data['email'])
        
        if not user:
            return redirect('/')
        if user.check_password(form.data['password']):
            login(request, user)
            user.is_active = True
            user.save()
            return redirect('/')
        return redirect('')
    