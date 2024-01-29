from django.urls import path
from userapp import views
app_name='userapp'

urlpatterns = [
    path('', views.registerpage,name='register'),
    path('login/', views.loginpage,name='login'),
    path('home/', views.home,name='home'),
    path('logout/', views.logoutuser,name='logout'),
    path('view_user_logs/', views.view_user_logs, name='view_user_logs'),
]    


