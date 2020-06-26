from django.shortcuts import render,redirect
from .models import user
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login,logout,authenticate

# Create your views here.
def manual(request):
    if request.user.is_authenticated:
        if request.user.type == 'doctor':
            return redirect('/home/doctor')
        else:
            return redirect('/home/patient')
    if request.method=='POST':
        try:
            u1=user.objects.get(email=request.POST['email'])
        except ObjectDoesNotExist:
            return render(request,'index.html',{'error':'User does not exist.'})
        raw_pass=request.POST['password'].lstrip()
        u1=authenticate(username=u1.username,password=raw_pass)
        if u1:
            login(request,u1)
            if u1.type == 'doctor':
                return redirect('/home/doctor')
            else:
                return redirect('/home/patient')
        else:
            return render(request,'index.html',{'error':'Incorrect Password'})
    else:
        return render(request,'index.html')

def log_out(request):
    logout(request)
    return redirect('/login/')