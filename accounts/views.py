from django.shortcuts import render,redirect
from accounts.forms import RegistrationForm
from .models import Account
from django.contrib import  messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username = username,password=password) 
            
            user.phone_number = phone_number
            user.save()
            
            messages.success(request, 'Registration Successfull')
            return redirect('register');
            
    else:
        form = RegistrationForm()

    context = {
        'form':form,
    }
    return render(request,'accounts/register.html',context)

def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email,password=password)
        
        if user is not None:
            login(request,user)
            # messages.success(request,'You are Now Logined In')
            return redirect('home')
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')


@login_required
def logout_user(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect('login')
