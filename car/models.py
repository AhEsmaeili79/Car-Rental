from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()

class Car(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='car_images/')
    image2 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    image4 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    image5 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    city = models.CharField(max_length=100)
    capacity = models.IntegerField()
    price_per_day = models.IntegerField()
    with_driver = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            img = img.resize((1000, 1000), Image.LANCZOS)
            img.save(img_path)


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('car', 'user')

    def __str__(self):
        return f'Review by {self.user.username} on {self.car.name}'