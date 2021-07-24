from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
import datetime
# Create your views here.
@login_required
def index(request):
    total_spent = 0
    total_recieved = 0

    expenditures = Expenditure.objects.filter(user=request.user)
    for i in expenditures:
        total_spent += i.amount_paid
    

    net_balance = total_recieved - total_spent

    cash_balance = request.user.profile.cash_balance
    bank_balance = request.user.profile.bank_balance
    return render(request, 'index.html', {
        "expenditures":expenditures,
        "total_spent": total_spent,
        "total_recieved": total_recieved,
        "net_balance": net_balance,
        "cash_balance": cash_balance,
        "bank_balance": bank_balance,
    })

@login_required
def bank_to_cash(request):
    if request.method == "POST":
        form = AddToCashForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > request.user.profile.bank_balance:
                messages.warning(request, "Cant process request, You don't have enough money balance in your Bank Balance.\nTry less amount.")
                return redirect("/bank/to/cash/")
            else:
                request.user.profile.bank_balance -= amount
                request.user.profile.cash_balance += amount
                request.user.profile.save()
                History.objects.create(
                    user = request.user,
                    amount = amount,
                    history_type = 3,
                    date = datetime.date.today()

                )
                messages.success(request, f"GH₵ {amount} has been successfully deducted from your Bank Blance and added to Cash Balance")
                return redirect("/")
    else:
        form = AddToCashForm()
    return render(request, "add_cash.html", {"form":form})

@login_required
def add_bank(request):
    if request.method == "POST":
        form = AddToBankForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            request.user.profile.bank_balance += amount
            request.user.profile.save()
            History.objects.create(
                    user = request.user,
                    amount = amount,
                    history_type = 2,
                    date = datetime.date.today()

                )
            messages.success(request, f"GH₵ {amount} has been successfully deposited to your Bank Balance.")
            return redirect("/")
    else:
        form = AddToBankForm()
    return render(request, "add_bank.html", {"form":form})


@login_required
def add_cash(request):
    if request.method == "POST":
        form = AddCashkForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            request.user.profile.cash_balance += amount
            request.user.profile.save()
            History.objects.create(
                    user = request.user,
                    amount = amount,
                    history_type = 1,
                    date = datetime.date.today()

                )
            messages.success(request, f"GH₵ {amount} has been successfully added to your Cash Balance.")
            return redirect("/")
    else:
        form = AddToBankForm()
    return render(request, "add_bank.html", {"form":form})

@login_required
def add_expenditure(request):
    if request.method == "POST":
        form = ExpenditureForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            payment_mode = form.cleaned_data['payment_mode']

            expenditure = form.save(commit=False)
            expenditure.user = request.user

            if payment_mode == 'Cash':
                request.user.profile.cash_balance -= expenditure.amount_paid
                request.user.profile.save()
                expenditure.save()
                messages.success(request, f"Expense of 'GH₵ {expenditure.amount_paid}' have beend added successfuly.")
                return redirect("/")
            elif payment_mode == 'Bank':
                request.user.profile.bank_balance -= expenditure.amount_paid
                request.user.profile.save()
                expenditure.save()
                messages.success(request, f"Expense of 'GH₵ {expenditure.amount_paid}' has successfuly been added.")
                return redirect("/")

        else:
            messages.warning(request, "Baby, theere was an error please try again. :(")

    else:
        form = ExpenditureForm()
    
    return render(request, "add_expenditure.html", {"form":form})


@login_required
def history(request):
    return render(request, 'history.html')


@login_required
def expenditure_history(request, year=None, month=None, day=None):

    if year and month and day:
        expenditures = Expenditure.objects.filter(date__year=year, date__month=month, date__day=day)
    elif year and month:
        expenditures = Expenditure.objects.filter(date__year=year, date__month=month)
    elif year:
        expenditures = Expenditure.objects.filter(date__year=year)
    else:
        expenditures = Expenditure.objects.all()
    

    total_expenditure = 0
    for x in expenditures:
        total_expenditure += x.amount_paid
    

    return render(request, 'expenditure_history.html', {
        "expenditures": expenditures,
        'year': year,
        'month': month,
        'day': day,
        "total_expenditure": total_expenditure,
    })

@login_required
def deposite_history(request, year=None, month=None, day=None):
    if year and month and day:
        deposites = Balance.objects.filter(date__year=year, date__month=month, date__day=day)
    elif year and month:
        deposites = Balance.objects.filter(date__year=year, date__month=month)
    elif year:
        deposites = Balance.objects.filter(date__year=year)
    else:
        deposites = Balance.objects.all()
    

    total_deposite = 0
    for x in deposites:
        total_deposite += x.amount
    
    return render(request, 'deposite_history.html', {
        "deposites": deposites,
        'year': year,
        'month': month,
        'day': day,
        "total_deposite": total_deposite,
    })
