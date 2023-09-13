from django.contrib import admin
from .models import Item

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "uuid", "name", "price", "date_created", "date_modified"]

admin.site.register(Item, ItemAdmin)