from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        min_length=3,
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_]+$',
                message='نام کاربری فقط می‌تواند شامل حروف انگلیسی، اعداد و علامت زیرخط باشد.'
            )
        ],
        error_messages={
            'required': 'نام کاربری الزامی است.',
            'min_length': 'نام کاربری باید حداقل ۳ کاراکتر باشد.',
            'max_length': 'نام کاربری نمی‌تواند بیشتر از ۱۵۰ کاراکتر باشد.',
        }
    )
    
    email = forms.EmailField(
        error_messages={
            'required': 'ایمیل الزامی است.',
            'invalid': 'لطفاً یک ایمیل معتبر وارد کنید.',
        }
    )
    
    
    password1 = forms.CharField(
        min_length=8,
        error_messages={
            'required': 'رمز عبور الزامی است.',
            'min_length': 'رمز عبور باید حداقل ۸ کاراکتر باشد.',
        }
    )
    
    password2 = forms.CharField(
        error_messages={
            'required': 'تأیید رمز عبور الزامی است.',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phonenumber', 'address']
        error_messages = {
            'first_name': {
                'required': 'نام الزامی است.',
                'max_length': 'نام نمی‌تواند بیشتر از ۳۰ کاراکتر باشد.',
            },
            'last_name': {
                'required': 'نام خانوادگی الزامی است.',
                'max_length': 'نام خانوادگی نمی‌تواند بیشتر از ۳۰ کاراکتر باشد.',
            },
            'address': {
                'required': 'آدرس الزامی است.',
                'max_length': 'آدرس نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد.',
            },
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلاً ثبت شده است.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('رمزهای عبور مطابقت ندارند. لطفاً دوباره تلاش کنید.')
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('رمز عبور باید حداقل شامل یک عدد باشد.')
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('رمز عبور باید حداقل شامل یک حرف بزرگ باشد.')
        return password1


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        error_messages={
            'required': 'نام کاربری الزامی است.',
        }
    )
    password = forms.CharField(
        error_messages={
            'required': 'رمز عبور الزامی است.',
        }
    )

    error_messages = {
        'invalid_login': 'نام کاربری یا رمز عبور اشتباه است.',
        'inactive': 'این حساب کاربری غیرفعال است.',
        'invalid_credentials': 'نام کاربری یا رمز عبور اشتباه است.',
        'too_many_attempts': 'تعداد تلاش‌های شما بیش از حد مجاز است. لطفاً چند دقیقه صبر کنید.',
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
