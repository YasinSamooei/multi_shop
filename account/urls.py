from django.urls import path
from . import views
app_name="account"

urlpatterns=[ 
    path("logout",views.logout_user,name="logout"),
    path("register/or/login",views.UserRegisterLogin.as_view(),name="register-login"),
    path("check/otp/code",views.CheckOtpView.as_view(),name="check-otp-code"),
    path("add/address",views.AddAddressView.as_view(),name="add-address"),
   
] 

 
