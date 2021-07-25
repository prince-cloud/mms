from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
import datetime
# Create your views here.

def signup(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user_form = form.save(commit=False)
            user_form.set_password(data["password"])
            user_form.save()
            Profile.objects.create(
                user=user_form,
            )
            form.save()
            messages.success(request, "account successfully created.")
            return redirect("/login")
        else:
            messages.warning(request, "Error in the form. Please check and try again.")
    else:
        form = RegisterForm()

    return render(request, "registration/signup.html", {"form":form})

def edit_account(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully updated")
            return redirect("/")
        else:
            messages.warning(request, "Error in the form. Please check and try again.")
    else:
        form = EditUserForm(instance=user)

    return render(request, "registration/edit_profile.html", {"form":form, "user":user})

@login_required
def index(request):
    total_spent = 0
    total_recieved = 0

    expenditures = Expenditure.objects.filter(user=request.user)
    for i in expenditures:
        total_spent += i.amount_paid

    net_balance = total_recieved - total_spent

    cash_balance = request.user.profile.cash_balance
    momo_balance = request.user.profile.momo_balance

    histories = History.objects.filter(user=request.user)
    return render(request, 'index.html', {
        "expenditures": expenditures,
        "total_spent": total_spent,
        "total_recieved": total_recieved,
        "net_balance": net_balance,
        "cash_balance": cash_balance,
        "momo_balance": momo_balance,
        "histories": histories,
    })


@login_required
def momo_to_cash(request):
    if request.method == "POST":
        form = AddToCashForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > request.user.profile.momo_balance:
                messages.warning(
                    request, "Cant process request, You don't have enough money balance in your Bank Balance.\nTry less amount.")
                return redirect("/bank/to/cash/")
            else:
                request.user.profile.momo_balance -= amount
                request.user.profile.cash_balance += amount
                request.user.profile.save()
                History.objects.create(
                    user=request.user,
                    amount=amount,
                    history_type=3,
                    date=datetime.date.today()

                )
                messages.success(
                    request, f"GH₵ {amount} has been successfully deducted from your Bank Blance and added to Cash Balance")
                return redirect("/")
    else:
        form = AddToCashForm()
    return render(request, "add_momo-cash.html", {"form": form})


@login_required
def add_momo(request):
    if request.method == "POST":
        form = AddToBankForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            request.user.profile.momo_balance += amount
            request.user.profile.save()
            History.objects.create(
                user=request.user,
                amount=amount,
                history_type=2,
                date=datetime.date.today()

            )
            messages.success(
                request, f"GH₵ {amount} has been successfully deposited to your Bank Balance.")
            return redirect("/")
    else:
        form = AddToBankForm()
    return render(request, "add_momo.html", {"form": form})


@login_required
def add_cash(request):
    if request.method == "POST":
        form = AddCashkForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            request.user.profile.cash_balance += amount
            request.user.profile.save()
            History.objects.create(
                user=request.user,
                amount=amount,
                history_type=1,
                date=datetime.date.today()

            )
            messages.success(
                request, f"GH₵ {amount} has been successfully added to your Cash Balance.")
            return redirect("/")
    else:
        form = AddToBankForm()
    return render(request, "add_cash.html", {"form": form})


@login_required
def add_expenditure(request):
    if request.method == "POST":
        form = ExpenditureForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            payment_mode = form.cleaned_data['payment_mode']

            expenditure = form.save(commit=False)
            expenditure.user = request.user

            if payment_mode == 'Cash':
                if request.user.profile.cash_balance < expenditure.amount_paid:
                    messages.warning(request, f'Your Cash is insuficient for this transaction.\nCash Balance: GH₵ {request.user.profile.cash_balance}')
                else:
                    request.user.profile.cash_balance -= expenditure.amount_paid
                    request.user.profile.save()
                    expenditure.save()
                    messages.success(
                        request, f"Expense of 'GH₵ {expenditure.amount_paid}' have beend added successfuly.")
                    History.objects.create(
                        user=request.user,
                        amount=expenditure.amount_paid,
                        history_type=4,
                        date=datetime.date.today()
                    )
                    return redirect("/")
            elif payment_mode == 'Momo':
                if request.user.profile.momo_balance < expenditure.amount_paid:
                    messages.warning(request, f'Your Momo Balance is insuficient for this transaction.\nMomo Balance: GH₵ {request.user.profile.momo_balance}')
                else:
                    request.user.profile.momo_balance -= expenditure.amount_paid
                    request.user.profile.save()
                    expenditure.save()
                    messages.success(
                        request, f"Expense of 'GH₵ {expenditure.amount_paid}' has successfuly been added.")
                    History.objects.create(
                        user=request.user,
                        amount=expenditure.amount_paid,
                        history_type=4,
                        date=datetime.date.today()
                    )
                    return redirect("/")

        else:
            messages.warning(
                request, "Baby, theere was an error please try again. :(")

    else:
        form = ExpenditureForm()

    return render(request, "add_expenditure.html", {"form": form})


@login_required
def history(request):
    if request.method == "POST":
        form = HistoryChoiceForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            option = form.cleaned_data['history_choice']
            if option == "ca":
                return redirect("/cash/history/")
            elif option == "m":
                return redirect("/momo/history/")
            elif option == "e":
                return redirect("/expenditure/history/")
            elif option == "mc":
                return redirect("/momo-cash/history/")
            elif option == "c":
                messages.warning(request, "Please select History Type")

    else:
        form = HistoryChoiceForm()
    return render(request, 'history.html', {"form": form})


@login_required
def expenditure_history(request, year=None, month=None, day=None):

    if year and month and day:
        expenditures = Expenditure.objects.filter(
            date__year=year, date__month=month, date__day=day, user=request.user)
    elif year and month:
        expenditures = Expenditure.objects.filter(
            date__year=year, date__month=month, user=request.user)
    elif year:
        expenditures = Expenditure.objects.filter(date__year=year, user=request.user)
    else:
        expenditures = Expenditure.objects.filter(user=request.user)

    total_expenditure = 0
    for x in expenditures:
        total_expenditure += x.amount_paid

    return render(request, 'history/expenditure_history.html', {
        "expenditures": expenditures,
        'year': year,
        'month': month,
        'day': day,
        "total_expenditure": total_expenditure,
    })


@login_required
def cash_history(request, year=None, month=None, day=None):
    if year and month and day:
        historys = History.objects.filter(
            date__year=year, date__month=month, date__day=day, user=request.user, history_type=1)
    elif year and month:
        historys = History.objects.filter(
            date__year=year, date__month=month, user=request.user, history_type=1)
    elif year:
        historys = History.objects.filter(
            date__year=year, user=request.user, history_type=1)
    else:
        historys = History.objects.filter(user=request.user, history_type=1)

    total = 0
    for x in historys:
        total += x.amount

    return render(request, 'history/cash_history.html', {
        "historys": historys,
        'year': year,
        'month': month,
        'day': day,
        "total": total,
    })


@login_required
def momo_history(request, year=None, month=None, day=None):
    if year and month and day:
        historys = History.objects.filter(
            date__year=year, date__month=month, date__day=day, user=request.user, history_type=2)
    elif year and month:
        historys = History.objects.filter(
            date__year=year, date__month=month, user=request.user, history_type=2)
    elif year:
        historys = History.objects.filter(
            date__year=year, user=request.user, history_type=2)
    else:
        historys = History.objects.filter(user=request.user, history_type=2)

    total = 0
    for x in historys:
        total += x.amount

    return render(request, 'history/momo_history.html', {
        "historys": historys,
        'year': year,
        'month': month,
        'day': day,
        "total": total,
    })


@login_required
def momo_to_cash_history(request, year=None, month=None, day=None):
    if year and month and day:
        historys = History.objects.filter(
            date__year=year, date__month=month, date__day=day, user=request.user, history_type=3)
    elif year and month:
        historys = History.objects.filter(
            date__year=year, date__month=month, user=request.user, history_type=3)
    elif year:
        historys = History.objects.filter(
            date__year=year, user=request.user, history_type=3)
    else:
        historys = History.objects.filter(user=request.user, history_type=3)

    total = 0
    for x in historys:
        total += x.amount

    return render(request, 'history/momo_to_cash_history.html', {
        "historys": historys,
        'year': year,
        'month': month,
        'day': day,
        "total": total,
    })
