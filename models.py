from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class GroceryItem(models.Model):
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    added_date = models.DateField()
    expiry_date = models.DateField()
    shelf_life_days = models.IntegerField()
    price = models.FloatField()

    def is_expired(self):
        from datetime import date
        return self.expiry_date < date.today()

    def status(self):
        from datetime import date, timedelta
        today = date.today()
        if self.expiry_date < today:
            return 'Expired'
        elif self.expiry_date <= today + timedelta(days=2):
            return 'Expiring Soon'
        return 'Fresh'
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(GroceryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.phone_number} - {self.product.item_name}"

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Optional: add name or email fields
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # Optional: ['email', 'name']

    def __str__(self):
        return self.phone_number
# Create your models here.
