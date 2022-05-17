from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .errors import ErrorMessages
from .models import CustomUser
from .forms import RegistrationForm, LoginForm


class RegisterView(View):
    """
        RegisterView provides operations for user registration.
        
        Attributes:
        ----------
        param template_name: Describes template name for render
        type template_name: str
        param form: Describes django-form for registration
        type form: RegistrationForm
    """
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
    """
        LoginView provides operations for user loging in.
        
        Attributes:
        ----------
        param template_name: Describes template name for render
        type template_name: str
        param form: Describes django-form for logining in
        type form: LoginForm
    """
    template_name = 'authentication/login.html'
    form = LoginForm
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})
    
    def post(self, request):
        form = self.form(request.POST)
        
        try:
            user = CustomUser.objects.get(email=form.data['email'])
        except ObjectDoesNotExist:
            user = None
        
        if not user or not user.check_password(form.data['password']):
            form.errors['email'] = form.error_class([ErrorMessages.USER_NOT_FOUND_ERROR])
            return render(request, self.template_name, {'form': form})
        
        login(request, user)
        user.is_active = True
        user.save()

        return redirect('/')


class LogoutView(View):
    """
        LogoutView provides opeartions for user logining out.
    """
    def get(self, request):
        if request.user.is_authenticated:
            request.user.is_active = False
            request.user.save()
            logout(request)
        return redirect('/')
