from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid


class BankAccount(models.Model):
    """Represents a linked bank account for ACH transfers"""
    ACCOUNT_TYPES = [
        ('checking', 'Checking'),
        ('savings', 'Savings'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPES)
    routing_number = models.CharField(max_length=9)  # ABA routing number
    account_number = models.CharField(max_length=17)  # Typically 10-12 digits
    institution_name = models.CharField(max_length=255)
    
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'routing_number', 'account_number')

    def __str__(self):
        return f"{self.institution_name} - {self.get_account_type_display()} ({self.account_number[-4:]})"

class ACHEntry(models.Model):
    """Represents an ACH transaction"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('settled', 'Settled'),
        ('failed', 'Failed'),
        ('returned', 'Returned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    source_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, related_name='source_transfers')
    destination_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, related_name='destination_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ACH {self.id}: ${self.amount} ({self.get_status_display()})"
    
    
class Transfer(models.Model):
    source_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, related_name='outgoing_transfers')
    destination_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, related_name='incoming_transfers')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # e.g., "completed", "failed"

    def __str__(self):
        return f"Transfer #{self.id}"

