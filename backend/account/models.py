from django.db import models
from customers.models import Customer

class Invoice(models.Model):
    customer = models.ForeignKey( 
        Customer,
        on_delete=models.CASCADE,
        related_name='invoices' 
    )
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.id} for {self.customer.identity_card_number} - Amount Due: ${self.amount_due}"