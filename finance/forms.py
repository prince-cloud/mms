from django import forms
from django.contrib.auth import get_user_model
from django.db.models import fields
from .models import *
User = get_user_model()

HISTORY_CHOICE = (
    ("c", "Choose an Option"),
    ("e", "Expenditure History"),
    ("ca", "Cash History"),
    ("m", "Momo History"),
    ("mc", "Momo-Cash History"),
)


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Re-enter password", widget=forms.PasswordInput, )
    password = forms.CharField(
        widget=forms.PasswordInput,  help_text="must be more than 6 characters")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

    def clean_password2(self, *args, **kwargs):
        data = self.cleaned_data
        p = data["password2"]
        p_1 = data["password"]
        if len(p) < 6:
            raise forms.ValidationError(
                "Your password should be 6 or more characters")
        if p == p_1:
            return p
        raise forms.ValidationError("Your passwords do not match")

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

class HistoryChoiceForm(forms.Form):
    history_choice = forms.ChoiceField(choices=HISTORY_CHOICE)


class ExpenditureForm(forms.ModelForm):
    quantity = forms.IntegerField(label='Quantity (Optional)', required=False)

    class Meta:
        model = Expenditure
        fields = (
            "description",
            "quantity",
            "amount_paid",
            "payment_mode",
        )


class AddToCashForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=100)


class AddToBankForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=100)


class AddCashkForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=100)
