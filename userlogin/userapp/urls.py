from django.urls import path
from userapp import views

urlpatterns = [
    path('register/', views.registerpage,name='register'),
    path('login/', views.loginpage,name='login'),
    path('', views.home,name='home'),
    path('logout/', views.logoutuser,name='logout'),


]