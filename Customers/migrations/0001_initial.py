# Generated by Django 4.2.5 on 2023-09-18 11:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(max_length=250, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=250, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=250, verbose_name='Phone Number')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date Modified')),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
        ),
    ]
