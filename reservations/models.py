from django.db import models
from car.models import Car
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    return_date = models.DateField()
    number_of_passengers = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ], default='pending')

    def __str__(self):
        return f"Order for {self.car.name} by {self.user.username}"
