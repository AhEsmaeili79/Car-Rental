from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from car.models import Car
from .models import Order
from .forms import OrderForm
from datetime import date, timedelta
from django.utils import timezone
import io
from PIL import Image

User = get_user_model()

def create_test_image():
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), 'white')
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=file.read(),
        content_type='image/jpeg'
    )

class OrderModelTest(TestCase):
    def setUp(self):
        # Create a test user (renter)
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test host
        self.host = User.objects.create_user(
            username='testhost',
            email='host@example.com',
            password='testpass123',
            role=2  # Host role
        )
        
        # Create a test car
        self.image = create_test_image()
        self.car = Car.objects.create(
            name='Test Car',
            image=self.image,
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.host
        )
        
        # Create test dates
        self.pickup_date = date.today()
        self.return_date = self.pickup_date + timedelta(days=3)
        
        # Create a test order
        self.order = Order.objects.create(
            car=self.car,
            user=self.user,
            pickup_date=self.pickup_date,
            return_date=self.return_date,
            number_of_passengers=2,
            total_price=300
        )

    def test_order_creation(self):
        self.assertEqual(self.order.car, self.car)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.pickup_date, self.pickup_date)
        self.assertEqual(self.order.return_date, self.return_date)
        self.assertEqual(self.order.number_of_passengers, 2)
        self.assertEqual(self.order.total_price, 300)
        self.assertEqual(self.order.status, 'pending')

    def test_order_str_method(self):
        expected_str = f"سفارش {self.car.name} توسط {self.user.username}"
        self.assertEqual(str(self.order), expected_str)

class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a test user (renter)
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test host
        self.host = User.objects.create_user(
            username='testhost',
            email='host@example.com',
            password='testpass123',
            role=2  # Host role
        )
        
        # Create a test car
        self.image = create_test_image()
        self.car = Car.objects.create(
            name='Test Car',
            image=self.image,
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.host
        )
        
        # Create test dates
        self.pickup_date = date.today()
        self.return_date = self.pickup_date + timedelta(days=3)
        
        # Create a test order
        self.order = Order.objects.create(
            car=self.car,
            user=self.user,
            pickup_date=self.pickup_date,
            return_date=self.return_date,
            number_of_passengers=2,
            total_price=300
        )

    def test_order_car_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reservations:order_car', kwargs={'pk': self.car.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car/car_detail.html')

    def test_order_car_view_post_valid(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'pickup_date': self.pickup_date,
            'return_date': self.return_date,
            'number_of_passengers': 2
        }
        response = self.client.post(reverse('reservations:order_car', kwargs={'pk': self.car.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful order

    def test_order_car_view_post_invalid_capacity(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'pickup_date': self.pickup_date,
            'return_date': self.return_date,
            'number_of_passengers': 10  # More than car capacity
        }
        response = self.client.post(reverse('reservations:order_car', kwargs={'pk': self.car.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'تعداد مسافران از ظرفیت خودرو بیشتر است')

    def test_cancel_order(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('reservations:cancel_order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)
        updated_order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(updated_order.status, 'cancelled')

    def test_user_orders_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reservations:user_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/user_orders.html')
        self.assertContains(response, 'Test Car')

    def test_host_reservations_view(self):
        self.client.login(username='testhost', password='testpass123')
        response = self.client.get(reverse('reservations:renter_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/renter_reservations.html')
        self.assertContains(response, 'Test Car')

class OrderIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a test user (renter)
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test host
        self.host = User.objects.create_user(
            username='testhost',
            email='host@example.com',
            password='testpass123',
            role=2  # Host role
        )
        
        # Create a test car
        self.image = create_test_image()
        self.car = Car.objects.create(
            name='Test Car',
            image=self.image,
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.host
        )

    def test_full_reservation_workflow(self):
        # Login as user
        self.client.login(username='testuser', password='testpass123')
        
        # Create a reservation
        pickup_date = date.today()
        return_date = pickup_date + timedelta(days=3)
        response = self.client.post(reverse('reservations:order_car', kwargs={'pk': self.car.pk}), {
            'pickup_date': pickup_date,
            'return_date': return_date,
            'number_of_passengers': 2
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify reservation was created
        order = Order.objects.filter(car=self.car, user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, 'pending')
        
        # Login as host and confirm the reservation
        self.client.login(username='testhost', password='testpass123')
        response = self.client.post(reverse('reservations:confirm_reservation', kwargs={'reservation_id': order.pk}))
        self.assertEqual(response.status_code, 302)
        
        # Verify reservation was confirmed
        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')
        
        # Login as user and check reservation status
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reservations:user_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Car')
        self.assertContains(response, 'تایید شده')

    def test_overlapping_reservations(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Create first reservation
        pickup_date = date.today()
        return_date = pickup_date + timedelta(days=3)
        response = self.client.post(reverse('reservations:order_car', kwargs={'pk': self.car.pk}), {
            'pickup_date': pickup_date,
            'return_date': return_date,
            'number_of_passengers': 2
        })
        self.assertEqual(response.status_code, 302)
        
        # Try to create overlapping reservation
        response = self.client.post(reverse('reservations:order_car', kwargs={'pk': self.car.pk}), {
            'pickup_date': pickup_date + timedelta(days=1),
            'return_date': return_date + timedelta(days=1),
            'number_of_passengers': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'این خودرو در تاریخ انتخاب شده رزرو شده است')
