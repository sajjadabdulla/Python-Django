from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    flag_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Attraction(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=240, unique=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    image_url = models.URLField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    opening_hours = models.CharField(max_length=200, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.name


class Meta:
    ordering = ['-created_at']

class Review(models.Model):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.attraction.name}"
    
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attraction = models.ForeignKey('Attraction', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    visit_date = models.DateField()
    number_of_tickets = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')

    def __str__(self):
        return f"{self.user.username} → {self.attraction.name} ({self.status})"