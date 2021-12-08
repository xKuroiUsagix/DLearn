from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from .models import CustomUser


class RegisterView(View):
    template_name = 'authentication/register.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = CustomUser.objects.create()
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password'))
        user.save()
        login(request, user)
        return redirect('/')
    