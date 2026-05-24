from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CUSTOMER = "customer"
    ADMIN = "admin"
    ROLE_CHOICES = [(CUSTOMER, "Customer"), (ADMIN, "Admin")]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    @property
    def is_admin_user(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.username
