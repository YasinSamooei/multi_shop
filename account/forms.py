from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from django.core.exceptions import ValidationError
from django.core import validators
from django import forms
from account.models import User
from .models import Address
#--------------------------------------------------------------------------------------
# User forms
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=' رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name','username','phone','image','is_active')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone',)

#---------------------------------------------------------------------------------------------------------------------------
class RegisterLoginForm(forms.Form):
    phone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter your phone number or your email'}),validators=[validators.MaxLengthValidator(50)])
    
    # def clean_phone(self):
    #     phone=self.cleaned_data.get('phone')
    #     if not phone.isnumeric():
    #         raise ValidationError('It is not allowed to use letters for mobile phone numbers',code='not allowed to use letters')
    #     return phone
#---------------------------------------------------------------------------------------------------------------------------
class CheckOtpForm(forms.Form):
    otpcode=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter your registration code'}),validators=[validators.MaxLengthValidator(4)])
    def clean_otpcode(self):
        otpcode=self.cleaned_data.get('otpcode')
        if not otpcode.isnumeric():
            raise ValidationError('It is not allowed to use letters for otpcode',code='not allowed to use letters')
        return otpcode
#---------------------------------------------------------------------------------------------------------------------------
class AddressCreationForm(forms.ModelForm):
    user=forms.IntegerField(required=False)
    class Meta:
        model=Address
        fields="__all__"