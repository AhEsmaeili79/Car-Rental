from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from car.models import Car
from .models import Order
from .forms import OrderForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime

User = get_user_model()

@login_required
def order_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.car = car

            # Check if car is available for the selected dates
            existing_orders = Order.objects.filter(
                car=car,
                return_date__gte=order.pickup_date,
                pickup_date__lte=order.return_date,
                status__in=['pending', 'confirmed']
            )
            if existing_orders.exists():
                messages.error(request, 'این خودرو در تاریخ انتخاب شده رزرو شده است.')
                return redirect('car:car_detail', pk=pk)
            
            # Validate number of passengers
            if order.number_of_passengers > car.capacity:
                messages.error(request, 'تعداد مسافران از ظرفیت خودرو بیشتر است.')
                return redirect('car:car_detail', pk=pk)
            
            # Validate dates
            if order.return_date <= order.pickup_date:
                messages.error(request, 'تاریخ برگشت باید بعد از تاریخ تحویل باشد.')
                return redirect('car:car_detail', pk=pk)

            if order.pickup_date < timezone.now().date():
                messages.error(request, 'تاریخ تحویل نمی‌تواند در گذشته باشد.')
                return redirect('car:car_detail', pk=pk)

            # Calculate total price
            days = (order.return_date - order.pickup_date).days
            order.total_price = car.price_per_day * days
            if car.with_driver:
                order.total_price += 100000  # Additional charge for driver
            order.save()
            
            messages.success(request, 'رزرو خودرو با موفقیت انجام شد.')
            return redirect('car:car_detail', pk=pk)  
    else:
        form = OrderForm()
    return render(request, 'car/car_detail.html', {'form': form, 'object': car})

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            messages.success(request, 'رزرو با موفقیت لغو شد.')
        else:
            messages.error(request, 'این رزرو قابل لغو نیست.')
        return redirect('reservations:user_orders')
    return render(request, 'reservations/confirm_cancel_order.html', {'order': order})

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'reservations/user_orders.html', {'orders': orders})

@login_required
def host_reservations(request):
    if request.user.role != 2:  # Check if user is a host
        return redirect('home')
    cars = Car.objects.filter(user=request.user)
    reservations = Order.objects.filter(car__in=cars).order_by('-created_at')
    return render(request, 'reservations/host_reservations.html', {'reservations': reservations})

@login_required
def confirm_order(request, pk):
    if request.user.role != 2:  # Only hosts can confirm orders
        return redirect('home')
    order = get_object_or_404(Order, pk=pk, car__user=request.user)
    if request.method == 'POST' and order.status == 'pending':
        order.status = 'confirmed'
        order.save()
        messages.success(request, 'رزرو با موفقیت تایید شد.')
    return redirect('reservations:host_reservations')

@login_required
def reject_order(request, pk):
    if request.user.role != 2:  # Only hosts can reject orders
        return redirect('home')
    order = get_object_or_404(Order, pk=pk, car__user=request.user)
    if request.method == 'POST' and order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'رزرو با موفقیت رد شد.')
    return redirect('reservations:host_reservations')

@login_required
def create_reservation(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Calculate total days and price
        days = (end_date - start_date).days
        total_price = days * car.price_per_day
        
        # Create the reservation
        Order.objects.create(
            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price
        )
        
        messages.success(request, 'درخواست رزرو شما با موفقیت ثبت شد.')
        return redirect('my_reservations')
        
    return render(request, 'reservations/create_reservation.html', {'car': car})

@login_required
def my_reservations(request):
    reservations = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})

@login_required
def renter_reservations(request):
    if request.user.role != 2:  # Check if user is a renter
        messages.error(request, 'شما دسترسی به این بخش را ندارید.')
        return redirect('home')
        
    reservations = Order.objects.filter(car__user=request.user).order_by('-created_at')
    return render(request, 'reservations/renter_reservations.html', {'reservations': reservations})

@login_required
def confirm_reservation(request, reservation_id):
    if request.user.role != 2:  # Only renters can confirm orders
        messages.error(request, 'شما دسترسی به این عملیات را ندارید.')
        return redirect('home')
        
    reservation = get_object_or_404(Order, id=reservation_id, car__user=request.user)
    reservation.status = 'confirmed'
    reservation.save()
    messages.success(request, 'رزرو با موفقیت تایید شد.')
    return redirect('reservations:renter_reservations')

@login_required
def reject_reservation(request, reservation_id):
    if request.user.role != 2:  # Only renters can reject orders
        messages.error(request, 'شما دسترسی به این عملیات را ندارید.')
        return redirect('home')
        
    reservation = get_object_or_404(Order, id=reservation_id, car__user=request.user)
    reservation.status = 'cancelled'
    reservation.save()
    messages.success(request, 'رزرو با موفقیت رد شد.')
    return redirect('reservations:renter_reservations')
