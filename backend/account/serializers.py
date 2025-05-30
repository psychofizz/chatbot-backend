from rest_framework import serializers
from .models import Invoice
from customers.models import Customer 

class InvoiceSerializer(serializers.ModelSerializer):
    customer_identity_card_number = serializers.SlugRelatedField(
        source='customer',
        slug_field='identity_card_number',
        queryset=Customer.objects.all()
    )

    class Meta:
        model = Invoice
        fields = [
            'id',
            'customer_identity_card_number',
            'amount_due',
            'issued_at',
            'is_paid'
        ]

class CreateInvoiceSerializer(serializers.Serializer):
    """
    Serializer
    It takes customer_identity_card_number and amount_due.
    """
    customer_identity_card_number = serializers.CharField(max_length=13) # 13 because Honduras id are 13 digits 0000-0000-00000
    amount_due = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_customer_identity_card_number(self, value):
        """
        Check if the customer exists.
        """
        if not Customer.objects.filter(identity_card_number=value).exists():
            raise serializers.ValidationError("Customer with this identity card number does not exist.")
        return value