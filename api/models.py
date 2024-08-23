from django.db import models

class Role(models.TextChoices):
    RECEPTIONIST = 'recepcionista', 'Recepcionista'
    GUEST = 'hóspede', 'Hóspede'

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    zip_code = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

class PersonalData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    document_number = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    personal_data = models.OneToOneField(PersonalData, null=True, blank=True, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, null=True, blank=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.RECEPTIONIST)


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=[
        ('vago', 'Vago'),
        ('ocupado', 'Ocupado'),
        ('reservado', 'Reservado'),
    ])
    price = models.BigIntegerField()


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices)
    qr_code = models.CharField(max_length=255, blank=True, null=True)
    qr_code_status = models.BooleanField(default=False)
