# Generated by Django 5.0.7 on 2024-08-24 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_zip_code_address_zipcode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('vago', 'Vago'), ('ocupado', 'Ocupado'), ('reservado', 'Reservado')], default='vago', max_length=20),
        ),
    ]
