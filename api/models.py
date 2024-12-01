from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = [("admin", "Admin"), ("user", "User")]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="api_users",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="api_users",
    )


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_tickets = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Ticket(models.Model):  # Ensure it inherits from models.Model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ticket")
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_ticket",
    )
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event.name} - {self.quantity}"
