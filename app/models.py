import re

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.


class Enum:
    roll = [("admin", "Admin"), ("user", "User")]


from django.contrib.auth.hashers import identify_hasher
from django.core.exceptions import ValidationError
import re


def validate_password(password):
    try:
        # If the password is already hashed, skip validation
        identify_hasher(password)
        return
    except ValueError:
        # Password is not hashed; validate it
        password_regex = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if not re.match(password_regex, password):
            raise ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, one number, "
                "and one special character.",
            )


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(
        max_length=255,
        validators=[validate_password],
    )  # (Hashed)
    role = models.CharField(max_length=10, choices=Enum.roll)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()


"""
Event:
id: Primary Key
name: CharField (Max 255 characters)
date: DateField
total_tickets: IntegerField
tickets_sold: IntegerField (default 0)
"""


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_tickets = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name


"""
Ticket:
id: Primary Key
user: ForeignKey to User
event: ForeignKey to Event
quantity: IntegerField (Number of tickets purchased)
purchase_date: DateTimeField (auto_now_add=True)
"""


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event.name} - {self.quantity}"
