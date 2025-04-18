from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from house.models import House
from .forms import SignUpForm, UserInfoForm
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    houses = House.objects.all()
    return render(request, 'users/home.html', {'houses': houses})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 3  
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'ثبت نام با موفقیت انجام شد.')
                return redirect('home')
        else:
            for error in form.non_field_errors():  
                messages.error(request, error)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('home')

    form = SignUpForm()
    return render(request, 'includes/modal.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
            return redirect('home')

    return render(request, 'includes/modal.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def user_info(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user_form = UserInfoForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'اطلاعات کاربری شما با موفقیت تغییر یافت.')
                return redirect('user_info')
        elif 'request_role_change' in request.POST:
            request.user.role_change_requested = True
            request.user.save()
            messages.success(request, 'درخواست میزبانی شما با موفقیت ارسال گردید.')
            return redirect('user_info')
    else:
        user_form = UserInfoForm(instance=request.user)
    
    return render(request, 'users/user_info.html', {
        'user_form': user_form,
    })

def article(request):
    return render(request, 'pages/article.html')

def aboutus(request):
    return render(request, 'pages/aboutus.html')