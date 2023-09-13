from django.db import models
import uuid

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey('Customers.Customer', on_delete=models.PROTECT, verbose_name='Customer')
    item = models.ForeignKey('Items.Item', on_delete=models.PROTECT, verbose_name='Item')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    date_created = models.DateTimeField(verbose_name='Date Created',auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name='Date Modified',auto_now=True)

    def _get_order_item_total(self):
        return self.item.price * self.quantity
    
    total = property(_get_order_item_total)

    def __str__(self):
        return str(self.customer)
    
    class Meta:
        verbose_name_plural = 'Orders'