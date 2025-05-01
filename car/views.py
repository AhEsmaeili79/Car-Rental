from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import  Car, Review
from .forms import  CarForm, ReviewForm 
from django.db.models import Avg

def car_list(request):
    cars = Car.objects.filter(is_active=True)

    # Search filter
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            cars = cars.filter(name__icontains=search)

    # Price filter
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            cars = cars.filter(price_per_day__lte=price)

    # Location filter
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            cars = cars.filter(city__icontains=location)

    # With driver filter
    if 'with_driver' in request.GET:
        with_driver = request.GET['with_driver']
        if with_driver:
            cars = cars.filter(with_driver=with_driver == 'true')

    # Capacity filter
    if 'capacity' in request.GET:
        capacity = request.GET['capacity']
        if capacity:
            cars = cars.filter(capacity__gte=capacity)

    # Sorting
    sort_by = request.GET.get('sort_by', '-id')  # Default sort by newest (using id)
    valid_sort_fields = [
        'name', 'city', 'price_per_day', 'capacity', 
        '-id', '-price_per_day', '-name', '-city', '-capacity'
    ]
    
    if sort_by not in valid_sort_fields:
        sort_by = '-id'  # Default to newest if invalid sort field

    cars = cars.order_by(sort_by)

    # Calculate average ratings for each car
    for car in cars:
        car.avg_rating = car.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        car.review_count = car.reviews.count()

    context = {
        'cars': cars,
        'current_filters': request.GET,  # Pass current filters to template
    }
    return render(request, 'car/car_list.html', context)


class CarDetailView(DetailView):
    model = Car
    template_name = 'car/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        
        cars = Car.objects.all()
        context['cars'] = cars
        context['range'] = range(1, 6)

        reviews = Review.objects.filter(car=car)
        
        mean_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else 0
        context['reviews'] = reviews
        context['mean_rating'] = mean_rating 

        
        for review in reviews:
            review.filled_stars = range(review.rating)
            review.empty_stars = range(5 - review.rating)

        
        if self.request.user.is_authenticated:
            user_review = Review.objects.filter(car=car, user=self.request.user).first()
            context['form'] = ReviewForm(instance=user_review) if user_review else ReviewForm()
        else:
            context['form'] = None

        return context

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        user_review = Review.objects.filter(car=car, user=request.user).first()
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
        else:
            messages.error(request, 'خطا در ثبت نظر.')
        return redirect('car:car_detail', pk=car.pk)


def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            return redirect('car:car_list')
    else:
        form = CarForm()
    return render(request, 'car/car_form.html', {'form': form})


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car/car_form.html'
    success_url = reverse_lazy('car:car_list')

    def get_queryset(self):
        return Car.objects.filter(user=self.request.user)


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'car/car_confirm_delete.html'
    success_url = reverse_lazy('car:car_list')

    def get_queryset(self):
        return Car.objects.filter(user=self.request.user)


def search(request):
    query = request.GET.get('q')
    if query:
        cars = Car.objects.filter(name__icontains=query)
    else:
        cars = Car.objects.all()
    return render(request, 'car/search_results.html', {'cars': cars, 'query': query})
