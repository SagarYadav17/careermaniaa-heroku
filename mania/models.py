from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

from django.utils import timezone
from merchant_app.models import Course

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_merchant(self, email, username, password, merchant_type):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_staff = False
        user.is_superuser = False
        user.is_student = False
        user.is_active = True
        user.is_merchant = True
        user.merchant_type = merchant_type
        user.save(using=self._db)
        return user

    def create_student(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_staff = False
        user.is_superuser = False
        user.is_merchant = False
        user.is_student = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    TYPES = (
        (0, None),
        (1, 'College'),
        (2, 'Coaching'),
        (3, 'Jobs')
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    registered_date = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    email = models.EmailField(max_length=250, unique=True, db_index=True)
    username = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    merchant_type = models.IntegerField(default=0, choices=TYPES)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    line1 = models.CharField(max_length=250, blank=False, null=False)
    city = models.CharField(max_length=250, default=None)
    apartment = models.CharField(max_length=250, default=None)
    building = models.CharField(max_length=250, default=None)
    landmark = models.CharField(max_length=250, default=None)
    district = models.CharField(
        max_length=250, blank=False, null=False, default=None)
    state = models.CharField(
        max_length=250, blank=False, null=False, default=None)
    pincode = models.CharField(
        max_length=250, blank=False, null=False, default=None)

    def __str__(self):
        return self.apartment + ", " + self.building + ", " + self.line1 + ", " + self.city


class Geolocation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    lat = models.DecimalField(
        decimal_places=2, max_digits=10, null=False, default=None)
    lng = models.DecimalField(
        decimal_places=2, max_digits=10, null=False, default=None)

    def __str__(self):
        return str(self.user)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=20, default="")
    mobile = models.CharField(max_length=15, default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    fees = models.CharField(max_length=10)
    registration_id = models.CharField(max_length=100, unique=True, default="")
    txn_id = models.CharField(max_length=100, default="")
    txn_amount = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.first_name + self.last_name

class FAQ(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return self.question