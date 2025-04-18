from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phonenumber', 'address']
        error_messages = {
            'username': {
                'required': 'نام کاربری الزامی است.',
                'invalid': 'نام کاربری معتبر وارد کنید.',
                'unique': 'این نام کاربری قبلاً ثبت شده است.',  
            },
            'password1': {
                'required': 'رمز عبور الزامی است.',
                'invalid': 'رمز عبور باید معتبر باشد.',
            },
            'password2': {
                'required': 'تأیید رمز عبور الزامی است.',
            },
            'email': {
                'required': 'ایمیل الزامی است.',
                'invalid': 'لطفاً یک ایمیل معتبر وارد کنید.',
                'unique': 'این ایمیل قبلاً ثبت شده است.',
            },
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلاً ثبت شده است.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('رمزهای عبور مطابقت ندارند. لطفاً دوباره تلاش کنید.')
        return password2


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'نام کاربری یا رمز عبور اشتباه است.',
        'inactive': 'این حساب کاربری غیرفعال است.',
    }

class RoleChangeRequestForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []  

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phonenumber', 'address']
        error_messages = {
            'first_name': {
                'required': 'نام الزامی است.',
                'invalid': 'نام معتبر وارد کنید.',
            },
            'last_name': {
                'required': 'نام خانوادگی الزامی است.',
                'invalid': 'نام خانوادگی معتبر وارد کنید.',
            },
            'email': {
                'required': 'ایمیل الزامی است.',
                'invalid': 'لطفاً یک ایمیل معتبر وارد کنید.',
            },
            'phonenumber': {
                'required': 'شماره تلفن الزامی است.',
                'invalid': 'شماره تلفن معتبر وارد کنید.',
            },
            'address': {
                'required': 'آدرس الزامی است.',
                'invalid': 'آدرس معتبر وارد کنید.',
            },
        }
