

# frontend/models.py
from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image_file = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

class Instrument(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='instrument_images/')
    description = models.TextField()

    def __str__(self):
        return self.name