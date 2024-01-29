from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import Createuserform
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from .models import UserLog

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        form = Createuserform()

        if request.method=='POST':
            form = Createuserform(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'account was created for '+user)
                return redirect('/login')

        context={'form':form}
        return render(request,'register.html',context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                request.session['login_time'] = datetime.now().isoformat()
                return redirect('/home')
            else:
                messages.info(request,'username or password is incorrect!!!')
        return render(request,"login.html")

def logoutuser(request):
    last_login_time = request.session.get('login_time')  
    UserLog.objects.create(user=request.user, login_time=last_login_time, logout_time=datetime.now())
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def home(request):
    login_time_str = request.session.get('login_time', datetime.now().isoformat())
    login_time = datetime.fromisoformat(login_time_str)

    current_time = datetime.now()
    time_spent = current_time - login_time
    request.session['time_spent'] = time_spent.total_seconds()
    
    my_dict = {
        'msg1': 'Login history',
        'login_time': login_time.strftime('%Y-%m-%d %H:%M:%S'),
        'logout_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'time_spent': str(time_spent),
        'total_time_spent': str(timedelta(seconds=request.session.get('time_spent', 0))),
    }
    return render(request, 'home.html', my_dict)

def view_user_logs(request,user_id):
    
    user = get_object_or_404(User, id=user_id)
    user_logs = UserLog.objects.filter(user=user)

    context = {
        'user': user,
        'user_logs': user_logs,
    }

    return render(request, 'view_user_logs.html', context)




   
