from django.db import models


# ==============================
# USER
# ==============================

class User(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    password = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


# ==============================
# ADMIN
# ==============================

class Admin(models.Model):

    username = models.CharField(
        max_length=100,
        unique=True
    )

    password = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.username


# ==============================
# SERVICE
# ==============================

class Service(models.Model):

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    duration = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.name


# ==============================
# APPOINTMENT
# ==============================

class Appointment(models.Model):

    customer_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    service = models.CharField(
        max_length=100
    )

    date = models.CharField(
        max_length=50
    )

    time = models.CharField(
        max_length=50
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=50,
        default="Booked"
    )

    payment_status = models.CharField(
        max_length=50,
        default="Pending"
    )

    def __str__(self):
        return self.customer_name


# ==============================
# PAYMENT
# ==============================

class Payment(models.Model):

    customer_name = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=50,
        blank=True
    )

    payment_status = models.CharField(
        max_length=50,
        default="Paid"
    )

    def __str__(self):
        return self.customer_name


# ==============================
# FEEDBACK
# ==============================

class Feedback(models.Model):

    customer_name = models.CharField(
        max_length=100
    )

    rating = models.IntegerField(
        default=0
    )

    message = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.customer_name


# ==============================
# COMBO
# ==============================

class Combo(models.Model):

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name