from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import Createuserform
from django.contrib import messages
# from django.contrib.auth.signals import user_logged_in, user_logged_out
from datetime import datetime, timedelta

# from django.contrib.admin.models import LogEntry
# from .models import YourModel 

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = Createuserform()

        if request.method=='POST':
            form = Createuserform(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'account was created for '+user)
                return redirect('login')

        context={'form':form}
        return render(request,'register.html',context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)

                request.session['login_time'] = datetime.now().isoformat()

                return redirect('home')
            else:
                messages.info(request,'username or password is incorrect!!!')
        return render(request,"login.html")

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    login_time_str = request.session.get('login_time', datetime.now().isoformat())
    login_time = datetime.fromisoformat(login_time_str)

    current_time = datetime.now()
    time_spent = current_time - login_time
    request.session['time_spent'] = time_spent.total_seconds()

    # Logout the user if there is no movement or usage for 10 minutes (adjust as needed)
    # if time_spent > timedelta(minutes=10):
    #     logout(request)
    #     return redirect('login')
    
    my_dict = {
        'msg1': 'Login time details',
        'login_time': login_time.strftime('%Y-%m-%d %H:%M:%S'),
        'logout_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'time_spent': str(time_spent),
        'total_time_spent': str(timedelta(seconds=request.session.get('time_spent', 0))),
    }
    return render(request, 'home.html', my_dict)






   

