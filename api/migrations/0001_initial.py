# Generated by Django 5.0.7 on 2024-08-22 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('zip_code', models.CharField(max_length=10)),
                ('street', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('vago', 'Vago'), ('ocupado', 'Ocupado'), ('reservado', 'Reservado')], max_length=20)),
                ('price', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.address')),
                ('personal_data', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.personaldata')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid')], max_length=20)),
                ('qr_code', models.CharField(blank=True, max_length=255, null=True)),
                ('qr_code_status', models.BooleanField(default=False)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.user')),
            ],
        ),
    ]
