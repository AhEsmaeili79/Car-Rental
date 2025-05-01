from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Car, Review
from .forms import CarForm, ReviewForm
import os
from PIL import Image
import io

User = get_user_model()

def create_test_image():
    # Create a new image with a simple color
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), 'white')
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=file.read(),
        content_type='image/jpeg'
    )

class CarModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test image
        self.image = create_test_image()
        
        # Create a test car
        self.car = Car.objects.create(
            name='Test Car',
            image=self.image,
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.user
        )

    def test_car_creation(self):
        self.assertEqual(self.car.name, 'Test Car')
        self.assertEqual(self.car.city, 'Test City')
        self.assertEqual(self.car.capacity, 4)
        self.assertEqual(self.car.price_per_day, 100)
        self.assertFalse(self.car.with_driver)
        self.assertTrue(self.car.is_active)
        self.assertEqual(self.car.user, self.user)

    def test_review_creation(self):
        review = Review.objects.create(
            car=self.car,
            user=self.user,
            rating=5,
            comment='Great car!'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great car!')
        self.assertEqual(review.car, self.car)
        self.assertEqual(review.user, self.user)

class CarViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create test image
        self.image = create_test_image()
        
        # Create test car
        self.car = Car.objects.create(
            name='Test Car',
            image=self.image,
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.user
        )

    def test_car_list_view(self):
        response = self.client.get(reverse('car:car_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car/car_list.html')
        self.assertContains(response, 'Test Car')

    def test_car_detail_view(self):
        response = self.client.get(reverse('car:car_detail', kwargs={'pk': self.car.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car/car_detail.html')
        self.assertContains(response, 'Test Car')

    def test_car_create_view(self):
        response = self.client.get(reverse('car:car_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car/car_form.html')

    def test_car_update_view(self):
        response = self.client.get(reverse('car:car_update', kwargs={'pk': self.car.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car/car_form.html')

    def test_car_delete_view(self):
        response = self.client.get(reverse('car:car_delete', kwargs={'pk': self.car.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car/car_confirm_delete.html')

class CarFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.image = create_test_image()

    def test_car_form_valid(self):
        form_data = {
            'name': 'Test Car',
            'city': 'Test City',
            'capacity': 4,
            'price_per_day': 100,
            'with_driver': False,
        }
        form_files = {
            'image': self.image
        }
        form = CarForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            'name': '',  # Empty name should be invalid
            'city': 'Test City',
            'capacity': 4,
            'price_per_day': 100,
            'with_driver': False,
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

class ReviewFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.image = create_test_image()
        
        self.car = Car.objects.create(
            name='Test Car',
            image=self.image,
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.user
        )

    def test_review_form_valid(self):
        form_data = {
            'rating': 5,
            'comment': 'Great car!'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid(self):
        form_data = {
            'rating': 6,  # Invalid rating (should be 1-5)
            'comment': 'Great car!'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

class IntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.image = create_test_image()
        
        self.car = Car.objects.create(
            name='Test Car',
            image=self.image,
            city='Test City',
            capacity=4,
            price_per_day=100,
            with_driver=False,
            user=self.user
        )

    def test_full_car_workflow(self):
        # Test car creation
        image = create_test_image()
        response = self.client.post(reverse('car:car_create'), {
            'name': 'New Test Car',
            'city': 'New City',
            'capacity': 5,
            'price_per_day': 150,
            'with_driver': True,
            'image': image
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

        # Test car listing
        response = self.client.get(reverse('car:car_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Test Car')

        # Test car detail view
        new_car = Car.objects.get(name='New Test Car')
        response = self.client.get(reverse('car:car_detail', kwargs={'pk': new_car.pk}))
        self.assertEqual(response.status_code, 200)

        # Test adding a review
        response = self.client.post(reverse('car:car_detail', kwargs={'pk': new_car.pk}), {
            'rating': 5,
            'comment': 'Excellent car!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful review

        # Verify review was created
        review = Review.objects.filter(car=new_car).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Excellent car!')

    def test_search_and_filter(self):
        # Test search functionality
        response = self.client.get(reverse('car:car_list') + '?search=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Car')

        # Test price filter
        response = self.client.get(reverse('car:car_list') + '?price=150')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Car')

        # Test location filter
        response = self.client.get(reverse('car:car_list') + '?location=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Car')

        # Test capacity filter
        response = self.client.get(reverse('car:car_list') + '?capacity=3')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Car')
