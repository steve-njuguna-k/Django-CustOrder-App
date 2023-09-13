from django.contrib import admin
from .models import Order

# Register your models here.
class OderAdmin(admin.ModelAdmin):
    list_display = ["id", "uuid", "customer", "item", "quantity", "total", "date_created", "date_modified"]

admin.site.register(Order, OderAdmin)