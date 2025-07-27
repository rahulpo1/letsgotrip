from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('vendor', 'Vendor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

# Tour Package
class TourPackage(models.Model):
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)
    image = models.ImageField(upload_to='package_images/')
    category = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    expiry_date = models.DateField()

    def __str__(self):
        return self.title

# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    number_of_people = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.title}"
