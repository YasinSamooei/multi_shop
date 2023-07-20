from django.shortcuts import redirect, render
from django.contrib.auth import login , logout, authenticate
from django.views import View
from .forms import RegisterLoginForm,CheckOtpForm , AddressCreationForm
import ghasedakpack
from random import randint
from .models import Otp, User
# from django.utils.crypto import get_random_string
from django.urls import reverse
from uuid import uuid4

sms=ghasedakpack.Ghasedak("")
backend='account.authentication.EmailAuthenticateBackend'

#---------------------------------------------------------------------------------------------------------

def logout_user(request):
    logout(request)
    return redirect('/')

#---------------------------------------------------------------------------------------------------------


class UserRegisterLogin(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            form=RegisterLoginForm()
            return render(request,"account/register.html",{"form":form})
    
    def post(self,request):
        form=RegisterLoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            # token=get_random_string(length=32)
            token=str(uuid4())
            randcode=randint(1000,9999)
            # sms.verification({'receptor':cd["phone"],'type':'1','template':'','param1':randcode})
            print(randcode)
            Otp.objects.create(phone=cd['phone'],code=randcode,token=token)
            return redirect(reverse('account:check-otp-code')+f'?token={token}')

        else:
            form.add_error("phone","The information entered is not correct")
        return render(request,"account/register.html",{"form":form})

#---------------------------------------------------------------------------------------------------------
class CheckOtpView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            form=CheckOtpForm()
            return render(request,"account/check-otp-code.html",{"form":form})

    def post(self,request):
        form=CheckOtpForm(request.POST)
        if form.is_valid():
            token=request.GET.get('token')
            otp=Otp.objects.get(token=token)
            # user=User.objects.create_user(phone=otp.phone)
            user,is_create=User.objects.get_or_create(phone=otp.phone)
            login(request,user,backend=backend)
            otp.delete()
            return redirect('/')

        else:
            form.add_error("otpcode","The information entered is not correct")
        return render(request,"account/check-otp-code.html",{"form":form})
#---------------------------------------------------------------------------------------------------------

class AddAddressView(View):
    def post(self,request):
        form=AddressCreationForm(request.POST)
        if form.is_valid():
            address=form.save(commit=False)
            address.user=request.user
            address.save()
        next_page=request.GET.get('next')
        if next_page:
            return redirect(next_page)
        return render(request,'account/add_address.html',{'form':form})
    
    def get(self,request):
        form=AddressCreationForm()
        return render(request,'account/add_address.html',{'form':form})