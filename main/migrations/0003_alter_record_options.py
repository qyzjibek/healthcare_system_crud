# Generated by Django 5.1.3 on 2024-11-18 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_country_diseasetype_users_disease_doctor_patients_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'managed': True},
        ),
    ]
