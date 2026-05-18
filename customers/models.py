from django.db import models

class Customer(models.Model):
    customer_company_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_phone_number = models.IntegerField()
    customer_city = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'



