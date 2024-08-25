from django.db import models


class Role(models.TextChoices):
    RECEPTIONIST = 'recepcionista', 'Recepcionista'
    GUEST = 'hóspede', 'Hóspede'


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    zipCode = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)


class PersonalData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    documentNumber = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    personalData = models.OneToOneField(PersonalData, null=True, blank=True, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, null=True, blank=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.RECEPTIONIST)


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.BigIntegerField()
    description = models.CharField(max_length=255, null=True, blank=True, default='')
    status = models.CharField(
        max_length=20,
        choices=[
            ('vago', 'Vago'),
            ('ocupado', 'Ocupado'),
            ('reservado', 'Reservado'),
        ],
        default='vago'
    )

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    startDate = models.DateField()
    endDate = models.DateField()
    qrCode = models.TextField(blank=True, null=True)
    qrCodeStatus = models.BooleanField(default=False)
    checkedOut = models.BooleanField(default=False)
