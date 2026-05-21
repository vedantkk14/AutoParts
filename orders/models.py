from django.db import models
from customers.models import Customer
from inventory.models import Inventory


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        SHIPPED   = 'shipped',   'Shipped'
        DELIVERED = 'delivered',  'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Customer',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Order Status',
    )
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        verbose_name='Subtotal',
    )
    discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=10.00,
        verbose_name='Discount %',
    )
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        verbose_name='Discount Amount',
    )
    final_total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        verbose_name='Final Total',
    )
    notes = models.TextField(blank=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'ORD-{self.id:05d} — {self.customer.customer_company_name}'

    @property
    def total_qty(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Order',
    )
    inventory_item = models.ForeignKey(
        Inventory,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Inventory Item',
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Unit Price',
    )
    line_total = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name='Line Total',
    )

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'{self.inventory_item.part_name} × {self.quantity}'
