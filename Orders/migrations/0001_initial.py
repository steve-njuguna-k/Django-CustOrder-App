# Generated by Django 4.2.5 on 2023-09-18 11:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Customers', '0001_initial'),
        ('Items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date Modified')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Customers.customer', verbose_name='Customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Items.item', verbose_name='Item')),
            ],
            options={
                'verbose_name_plural': 'Orders',
            },
        ),
    ]
