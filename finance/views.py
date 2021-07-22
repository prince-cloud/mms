from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.
@login_required
def index(request):
    total_spent = 0
    total_recieved = 0

    expenditures = Expenditure.objects.all()
    for i in expenditures:
        total_spent += i.amount_paid
    
    balance = Balance.objects.filter(approved=True)
    for j in balance: 
        total_recieved += j.amount

    net_balance = total_recieved - total_spent
    return render(request, 'index.html', {
        "expenditures":expenditures,
        "total_spent": total_spent,
        "total_recieved": total_recieved,
        "net_balance": net_balance,
    })

@login_required
def add_expenditure(request):
    if request.method == "POST":
        form = ExpenditureForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            expenditure = form.save(commit=False)
            expenditure.user = request.user
            expenditure.save()
            messages.success(request, f"Expense of 'GH₵ {expenditure.amount_paid}' have beend added successfuly. :)")
            return redirect("/")
        else:
            messages.warning(request, "Baby, theere was an error please try again. :(")

    else:
        form = ExpenditureForm()
    
    return render(request, "add_expenditure.html", {"form":form})


@login_required
def deposite(request):
    if request.method == "POST":
        form = DepositeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            deposite = form.save(commit=False)
            deposite.user = request.user
            deposite.save()
            messages.success(request, f"An ammount of 'GH₵ {deposite.amount}' is pending approval from your partner.")
            return redirect("/")
        else:
            messages.warning(request, "Baby, theere was an error please try again. :(")

    else:
        form = DepositeForm()
    
    return render(request, "deposite.html", {"form":form})

@login_required
def approve_deposite(request, pk):
    deposite = get_object_or_404(Balance, pk=pk)
    amount = deposite
    amount.approved = True
    amount.save()
    messages.success(request, f"You approved an amount of 'GH₵ {deposite.amount}' and have been succesffuly added to your balance.")
    return redirect("/")

@login_required
def approvals(request):
    approvals = Balance.objects.filter(approved=False).exclude(user=request.user)
    return render(request, "approvals.html", {"approvals":approvals})

@login_required
def history(request):
    return render(request, 'history.html')

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
