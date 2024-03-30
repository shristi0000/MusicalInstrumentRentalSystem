

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
    image = models.ImageField(upload_to='instrument_images/',null=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    is_available = models.BooleanField(default=True)
    status = models.CharField(
        max_length=255,
        choices=[
            ("Pending", "Pending"),
            ("Rented", "Rented"),
            ("Returned", "Returned"),
            ("Available", "Available"),
            (" NOT Available", "NOT Available"),
            
        ],
       null=True
    )
    def __str__(self):
        return self.name
    
class  PasswordResetForm(models.Model):
     new_Password = models.CharField(max_length=100)
     new_Password = models.CharField(max_length=50)

class RentInstruments(models.Model):
    instrument = models.ForeignKey(Instrument,on_delete=models.CASCADE)
    renter= models.ForeignKey(User,on_delete=models.CASCADE)
    pickup_date= models.DateField()
    dropoff_date= models.DateField()
    pickup_address= models.TextField()
    dropoff_address=models.TextField()
    date= models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=255,
        choices=[
            ("Accepted","Accepted"),
            ("Declined","Declined"),
            ("Cancelled","Cancelled"),
            ("Pending","Pending"),
        ],
        default='pending'
    )


    

    