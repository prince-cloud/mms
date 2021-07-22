from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import DecimalField
User = get_user_model()

# Create your models here.
class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date",)
    
    def __str__(self):
        return str(self.user)

class Expenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(null=True, blank=True)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date",)
    
    def __str__(self):
        return self.description
