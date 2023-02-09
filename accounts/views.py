from django.shortcuts import render,redirect
from accounts.forms import RegistrationForm
from .models import Account
from django.contrib import  messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
# verification email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart,CartItem


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
            
            #user avitvation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)               
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
           

            return redirect('/accounts/login/?command=verification&email=' + email);
            
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
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                        
                    cart_item = CartItem.objects.filter(user=user)
                    # existing variation
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id['index']
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            login(request,user)
            messages.success(request,'You are Now Logined In')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # print('query -> ',query)
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
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


def activate(request, uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! Your account is activate.')
        return redirect('login')
    else: 
        messages.error(request,'Invalid activation link')
        return redirect('register')


@login_required
def dashboard(request):
    return render(request,'accounts/dashboard.html')


def forgetpassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)               
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            messages.success(request,"Password reset email has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request,'Account Does Not Exists')        
            return redirect('forgetpassword')
    return render(request,'accounts/forgetpassword.html')

def resetpassword_validate(request, uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Reset Your Password ')
        return redirect('resetpassword')
    else: 
        messages.error(request,'This link has been expired')
        return redirect('login')
    
    
def resetpassword(request):
    if request.method == "POST":
        password =  request.POST['password']
        confirmpassword =  request.POST['confirmpassword']
        if password == confirmpassword:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfull')
            return redirect('login')
        else:
            messages.error(request,'Password Do Not Match')
            return redirect('resetpassword')
    else:   
        return render(request,'accounts/resetpassword.html')