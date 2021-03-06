from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import DecimalField
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import NumberInput
User = get_user_model()

# Create your models here.

PAYMENT_MODE = (
    ('Cash', 'Cash'),
    ('Momo', 'Momo'),
)

HISTORY_TYPE = (
    ("1", "Add Cash"),
    ("2", "Add Bank"),
    ("3", "Bank To Cash"),
    ("4", "Expenditure"),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    momo_balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    cash_balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)
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
        return "".join([str(self.user), " - ",self.description, " - ", str(self.amount_paid)])

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='history')
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    history_type = models.CharField(choices=HISTORY_TYPE, max_length=100)
    expenditure_description = models.CharField(max_length=200, null=True, blank=True)
    received_from = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__ (self):
        return "".join([str(self.user), "'s transaction of ???" ,str(self.amount), " - ",str(self.history_type)])