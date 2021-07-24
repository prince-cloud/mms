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
            "payment_mode",
        )

class  AddToCashForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=100)

class  AddToBankForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=100)
class  AddCashkForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=100)



""" class DepositeForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = (
            "balance",
        ) """

""" class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ("amount",) """