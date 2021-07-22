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
            messages.success(request, f"Expense of 'GH₵ {deposite.amount_paid}' have beend added successfuly. :)")
            return redirect("/")
        else:
            messages.warning(request, "Baby, theere was an error please try again. :(")

    else:
        form = DepositeForm()
    
    return render(request, "deposite.html", {"form":form})
