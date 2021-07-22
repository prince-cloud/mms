from django import forms
from django.contrib.auth import get_user_model
from django.db.models import fields
from .models import *
User = get_user_model()


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = (
            "description",
            "quantity",
            "amount_paid",
        )

class DepositeForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = (
            "amount",
        )