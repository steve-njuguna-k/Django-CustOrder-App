from django.contrib import admin
from .models import Customer

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "uuid", "first_name", "last_name", "phone_number", "date_created", "date_modified"]

admin.site.register(Customer, CustomerAdmin)