from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.views import LoginView
from .models import User, EmailVerification
from django.contrib import auth
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponseRedirect


# Create your views here.
class MyLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        user = User.objects.get(username=username)
        if user.is_verifield_email==False:
            print('Ваш email не подтвержден')
            form.add_error('username', 'Ваш email не подтвержден.')
            return self.form_invalid(form)
        else:
            return super().form_valid(form)
    
  
class UserRegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    form_class = UserRegisterForm

    def form_valid(self, form):
        if User.objects.filter(email=form.cleaned_data['email']).exists():
            form.add_error('email', 'Такой email уже зарегистрирован.')
            return self.form_invalid(form)
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            form.add_error('username', 'Такой логин уже зарегистрирован.')
            return self.form_invalid(form)
        return super().form_valid(form)



def logout(request):
    auth.logout(request)
    return redirect('movies:index')



class EmailVerificationView(TemplateView):
    title = 'Store - Подтерждение электронной почты'
    template_name = 'users/email_verification.html'
    
    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verifield_email = True
            user.save()
            return super(EmailVerificationView,self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))