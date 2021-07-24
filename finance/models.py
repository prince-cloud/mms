from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import DecimalField
from django.forms.widgets import NumberInput
User = get_user_model()

# Create your models here.

PAYMENT_MODE = (
    ('Cash', 'Cash'),
    ('Bank', 'Bank'),
)

HISTORY_TYPE = (
    ("1", "Add Cash"),
    ("2", "Add Bank"),
    ("3", "Bank To Cash"),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bank_balance = models.DecimalField(max_digits=100, decimal_places=2)
    cash_balance = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-date",)
    
    def __str__(self):
        return str(self.user)


class Expenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(null=True, blank=True)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=100)
    payment_mode = models.CharField(choices=PAYMENT_MODE, max_length=6)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date",)
    
    def __str__(self):
        return self.description

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='history')
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    history_type = models.CharField(choices=HISTORY_TYPE, max_length=100)

    date = models.DateTimeField(auto_now_add=True)