from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('verify/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='email_verifications'),
   
]