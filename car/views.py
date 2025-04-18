from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import  House, Review
from .forms import  HouseForm, ReviewForm 
from django.db.models import Avg

def house_list(request):
    houses = House.objects.all()

    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            houses = houses.filter(price_per_day__lte=price)

    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            houses = houses.filter(city__icontains=location)

    sort_by = request.GET.get('sort_by', '-id') 
    if sort_by not in ['name', 'city', 'price_per_day', 'number_of_rooms', 'area']:
        sort_by = '-id'  

    houses = houses.order_by(sort_by)

    context = {
        'houses': houses,
    }
    return render(request, 'vila/vila_list.html', context)


class HouseDetailView(DetailView):
    model = House
    template_name = 'vila/vila_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = self.get_object()
        
        houses = House.objects.all()
        context['houses'] = houses
        context['range'] = range(1, 6)

        reviews = Review.objects.filter(house=house)
        
        mean_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else 0
        context['reviews'] = reviews
        context['mean_rating'] = mean_rating 

        
        for review in reviews:
            review.filled_stars = range(review.rating)
            review.empty_stars = range(5 - review.rating)

        
        if self.request.user.is_authenticated:
            user_review = Review.objects.filter(house=house, user=self.request.user).first()
            context['form'] = ReviewForm(instance=user_review) if user_review else ReviewForm()
        else:
            context['form'] = None

        return context

    def post(self, request, *args, **kwargs):
        house = self.get_object()
        user_review = Review.objects.filter(house=house, user=request.user).first()
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.house = house
            review.user = request.user
            review.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
        else:
            messages.error(request, 'خطا در ثبت نظر.')
        return redirect('house_detail', pk=house.pk)


def house_create(request):
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            house.user = request.user
            house.save()
            return redirect('host_houses')
    else:
        form = HouseForm()
    return render(request, 'vila/house_form.html', {'form': form})


class HouseUpdateView(LoginRequiredMixin, UpdateView):
    model = House
    form_class = HouseForm
    template_name = 'vila/house_form.html'
    success_url = reverse_lazy('house_list')

    def get_queryset(self):
        return House.objects.filter(user=self.request.user)


class HouseDeleteView(LoginRequiredMixin, DeleteView):
    model = House
    template_name = 'vila/house_confirm_delete.html'
    success_url = reverse_lazy('house_list')

    def get_queryset(self):
        return House.objects.filter(user=self.request.user)


def search(request):
    query = request.GET.get('q')
    if query:
        houses = House.objects.filter(name__icontains=query)
    else:
        houses = House.objects.all()
    return render(request, 'vila/search_results.html', {'houses': houses, 'query': query})
