from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from car.models import Car
from .models import Order
from .forms import OrderForm
from datetime import date, timedelta
import decimal

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role=3  # Passenger
        )
        
        # Create test host
        self.host = User.objects.create_user(
            username='testhost',
            password='testpass123',
            role=2  # Host
        )
        
        # Create test car
        self.car = Car.objects.create(
            name='Test Car',
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.host
        )
        
        # Create test order
        self.order = Order.objects.create(
            car=self.car,
            user=self.user,
            pickup_date=date.today() + timedelta(days=1),
            return_date=date.today() + timedelta(days=3),
            number_of_passengers=2,
            total_price=decimal.Decimal('200.00'),
            status='pending'
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.car, self.car)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.number_of_passengers, 2)
    
    def test_order_str(self):
        expected_str = f"Order for {self.car.name} by {self.user.username}"
        self.assertEqual(str(self.order), expected_str)
    
    def test_order_total_price_calculation(self):
        days = (self.order.return_date - self.order.pickup_date).days
        expected_price = self.car.price_per_day * days
        self.assertEqual(self.order.total_price, expected_price)

class OrderFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            'pickup_date': date.today() + timedelta(days=1),
            'return_date': date.today() + timedelta(days=3),
            'number_of_passengers': 2
        }
    
    def test_order_form_valid(self):
        form = OrderForm(data=self.form_data)
        self.assertTrue(form.is_valid())
    
    def test_order_form_invalid_dates(self):
        self.form_data['return_date'] = date.today()
        self.form_data['pickup_date'] = date.today() + timedelta(days=1)
        form = OrderForm(data=self.form_data)
        self.assertFalse(form.is_valid())
    
    def test_order_form_invalid_passengers(self):
        self.form_data['number_of_passengers'] = 0
        form = OrderForm(data=self.form_data)
        self.assertFalse(form.is_valid())

class OrderViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role=3  # Passenger
        )
        
        # Create test host
        self.host = User.objects.create_user(
            username='testhost',
            password='testpass123',
            role=2  # Host
        )
        
        # Create test car
        self.car = Car.objects.create(
            name='Test Car',
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.host
        )
        
        # Login the test user
        self.client.login(username='testuser', password='testpass123')
    
    def test_order_car_view_get(self):
        response = self.client.get(reverse('reservations:order_car', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car/car_detail.html')
    
    def test_order_car_view_post_valid(self):
        data = {
            'pickup_date': date.today() + timedelta(days=1),
            'return_date': date.today() + timedelta(days=3),
            'number_of_passengers': 2
        }
        response = self.client.post(reverse('reservations:order_car', args=[self.car.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Order.objects.filter(car=self.car, user=self.user).exists())
    
    def test_order_car_view_post_invalid_dates(self):
        data = {
            'pickup_date': date.today() + timedelta(days=3),
            'return_date': date.today() + timedelta(days=1),
            'number_of_passengers': 2
        }
        response = self.client.post(reverse('reservations:order_car', args=[self.car.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirect after error
        self.assertFalse(Order.objects.filter(car=self.car, user=self.user).exists())
    
    def test_user_orders_view(self):
        # Create a test order
        Order.objects.create(
            car=self.car,
            user=self.user,
            pickup_date=date.today() + timedelta(days=1),
            return_date=date.today() + timedelta(days=3),
            number_of_passengers=2,
            total_price=decimal.Decimal('200.00')
        )
        
        response = self.client.get(reverse('reservations:user_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/user_orders.html')
        self.assertEqual(len(response.context['orders']), 1)
    
    def test_host_reservations_view(self):
        # Login as host
        self.client.logout()
        self.client.login(username='testhost', password='testpass123')
        
        # Create a test order
        Order.objects.create(
            car=self.car,
            user=self.user,
            pickup_date=date.today() + timedelta(days=1),
            return_date=date.today() + timedelta(days=3),
            number_of_passengers=2,
            total_price=decimal.Decimal('200.00')
        )
        
        response = self.client.get(reverse('reservations:host_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/host_reservations.html')
        self.assertEqual(len(response.context['reservations']), 1)
    
    def test_cancel_order_view(self):
        # Create a test order
        order = Order.objects.create(
            car=self.car,
            user=self.user,
            pickup_date=date.today() + timedelta(days=1),
            return_date=date.today() + timedelta(days=3),
            number_of_passengers=2,
            total_price=decimal.Decimal('200.00')
        )
        
        response = self.client.post(reverse('reservations:cancel_order', args=[order.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')
