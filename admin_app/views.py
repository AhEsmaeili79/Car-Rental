from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from car.models import Car
from reservations.models import Order
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('home')

    # Get counts for dashboard
    total_users = User.objects.count()
    total_cars = Car.objects.count()
    total_orders = Order.objects.count()
    pending_renter_requests = User.objects.filter(role_change_requested=True).count()

    # Get all users
    users = User.objects.all()

    # Get all cars
    cars = Car.objects.all().order_by('-id')  # Order by id descending

    # Get all orders
    orders = Order.objects.all().order_by('-created_at')

    # Get renter requests
    renter_requests = User.objects.filter(role_change_requested=True)

    # Get recent activities (last 7 days)
    recent_activities = []
    for order in Order.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)):
        recent_activities.append({
            'timestamp': order.created_at,
            'user': order.user.username,
            'action': 'سفارش جدید',
            'status': order.get_status_display()
        })

    context = {
        'total_users': total_users,
        'total_cars': total_cars,
        'total_orders': total_orders,
        'pending_renter_requests': pending_renter_requests,
        'recent_activities': recent_activities[:10],  # Show only last 10 activities
        'users': users,
        'cars': cars,
        'orders': orders,
        'renter_requests': renter_requests,
    }

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == 'add_admin':
            new_admin_username = request.POST.get('new_admin_username')
            try:
                new_admin = User.objects.get(username=new_admin_username)
                new_admin.is_staff = True
                new_admin.save()
                messages.success(request, 'کاربر به عنوان مدیر افزوده شد.')
            except User.DoesNotExist:
                messages.error(request, 'کاربری با این نام کاربری وجود ندارد.')

        elif action_type == 'delete_car':
            car_id = request.POST.get('car_id')
            car = get_object_or_404(Car, id=car_id)
            car.delete()
            messages.success(request, 'خودرو با موفقیت حذف شد.')

        elif action_type == 'delete_order':
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            messages.success(request, 'سفارش با موفقیت حذف شد.')

        elif action_type == 'toggle_user_status':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.is_active = not user.is_active
            user.save()
            messages.success(request, f'کاربر {"فعال" if user.is_active else "غیرفعال"} شد.')

        elif action_type == 'toggle_car_status':
            car_id = request.POST.get('car_id')
            car = get_object_or_404(Car, id=car_id)
            car.is_active = not car.is_active
            car.save()
            messages.success(request, f'خودرو {"فعال" if car.is_active else "غیرفعال"} شد.')

        elif action_type == 'handle_renter_request':
            user_id = request.POST.get('user_id')
            approve = request.POST.get('approve') == 'true'
            user = get_object_or_404(User, id=user_id)
            if approve:
                user.role = 2
            user.role_change_requested = False
            user.save()
            messages.success(request, 'درخواست تغییر نقش کاربر پردازش شد.')

        return redirect('admin_panel')  

    return render(request, 'admin/admin_panel.html', context)

@login_required
def admin_users(request):
    if not request.user.is_superuser:
        return redirect('home')

    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role_filter', '')

    users = User.objects.all()

    if search_query:
        users = users.filter(username__icontains=search_query)

    if role_filter:
        if role_filter == 'admin':
            users = users.filter(is_superuser=True)
        elif role_filter == 'renter':
            users = users.filter(role=2)
        elif role_filter == 'user':
            users = users.filter(role=1)

    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)

    return render(request, 'admin/admin_users.html', {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter
    })

@login_required
def admin_orders(request):
    if not request.user.is_superuser:
        return redirect('home')

    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status_filter', '')

    orders = Order.objects.all().order_by('-created_at')

    if search_query:
        orders = orders.filter(user__username__icontains=search_query)

    if status_filter:
        orders = orders.filter(status=status_filter)

    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    return render(request, 'admin/admin_orders.html', {
        'orders': orders,
        'search_query': search_query,
        'status_filter': status_filter
    })

@login_required
def admin_cars(request):
    if not request.user.is_superuser:
        return redirect('home')

    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status_filter', '')

    cars = Car.objects.all().order_by('-id')  # Order by id descending

    if search_query:
        cars = cars.filter(name__icontains=search_query)

    if status_filter:
        cars = cars.filter(is_active=status_filter == 'active')

    paginator = Paginator(cars, 10)
    page = request.GET.get('page')
    cars = paginator.get_page(page)

    return render(request, 'admin/admin_cars.html', {
        'cars': cars,
        'search_query': search_query,
        'status_filter': status_filter
    })

def renter_cars(request):
    if request.user.is_authenticated and request.user.role == 2:
        renter_cars = Car.objects.filter(user=request.user)
        return render(request, 'admin/renter_cars.html', {'renter_cars': renter_cars})
    else:
        return render(request, 'admin/access_denied.html')  

@login_required
def admin_delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, 'خودرو با موفقیت حذف شد.')
    return redirect('admin_panel')  

@login_required
def toggle_car_status(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    car.is_active = not car.is_active
    car.save()
    messages.success(request, f'خودرو {"فعال" if car.is_active else "غیرفعال"} شد.')
    return redirect('admin_panel')  

@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    context = {
        'car': car,
    }
    return render(request, 'admin/car_detail.html', context)

@login_required
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    
    # Check if the user is either the car owner or a superuser
    if not (request.user == car.user or request.user.is_superuser):
        return redirect('home')
    
    if request.method == 'POST':
        # Update car fields
        car.name = request.POST.get('name')
        car.model = request.POST.get('model')
        car.daily_price = request.POST.get('daily_price')
        car.description = request.POST.get('description')
        
        # Handle image upload if provided
        if 'image' in request.FILES:
            car.image = request.FILES['image']
            
        car.save()
        messages.success(request, 'خودرو با موفقیت بروزرسانی شد.')
        return redirect('renter_cars')
        
    return render(request, 'admin/car_update.html', {'car': car})

@login_required
def renter_requests(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(User, id=user_id)
        
        if action == 'approve':
            user.role = 2  # Set role to renter
            messages.success(request, 'درخواست اجاره‌دهی کاربر تایید شد.')
        elif action == 'reject':
            messages.info(request, 'درخواست اجاره‌دهی کاربر رد شد.')
            
        user.role_change_requested = False
        user.save()
        return redirect('renter_requests')

    users_requesting_role_change = User.objects.filter(role_change_requested=True)
    return render(request, 'admin/renter_requests.html', {'users': users_requesting_role_change})

@login_required
def toggle_user_status(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')
        
    user = get_object_or_404(User, pk=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'کاربر {"فعال" if user.is_active else "غیرفعال"} شد.')
    return redirect('admin_panel')

@login_required
def admin_delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')
        
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'کاربر با موفقیت حذف شد.')
    return redirect('admin_panel')

@login_required
def admin_delete_order(request, order_id):
    if not request.user.is_superuser:
        return redirect('home')
        
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, 'سفارش با موفقیت حذف شد.')
    return redirect('admin_panel')