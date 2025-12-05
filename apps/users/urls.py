from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login_signup/', views.login_signup_view, name='login_signup'),
    path('login/', views.login_signup_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
