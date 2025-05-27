from django.db import models

class Customer(models.Model):
    """
    A basic customer

    This model stores basic customer details including their full name,
    phone number, and a unique identity card number.
    """
    full_name = models.CharField(
        max_length=255,
        verbose_name="Full Name",
        help_text="The customer's full name."
    )
    phone_number = models.CharField(
        max_length=8, 
        blank=True,    
        null=True,     
        verbose_name="Phone Number",
        help_text="8 digit telephone number like Tigo or Claro numbers (e.g., 9900-9950)" 
    )
    identity_card_number = models.CharField(
        max_length=13,  
        unique=True,    
        verbose_name="Number of Identity Card",
        help_text="Honduran identity card number (e.g., 0801-1999-00001) but like without hyphens"
    )

    class Meta:
        """
        Meta options for the Customer model.
        """
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['full_name'] 

    def __str__(self):
        """
        String representation of the Customer object.
        """
        return self.full_name
