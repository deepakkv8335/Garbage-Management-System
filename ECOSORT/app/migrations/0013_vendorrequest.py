# Generated by Django 5.0.6 on 2025-02-10 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_booking_healthassistant_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
    ]
