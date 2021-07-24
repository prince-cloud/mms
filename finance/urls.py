from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'finance'


urlpatterns = [
    path("", views.index, name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('add_expenditure/', views.add_expenditure, name="add_expenditure"),
    path('history/', views.history, name="history"),
    path('expenditure/history/', views.expenditure_history, name="expenditure_history"),
    path('deposite/history/', views.deposite_history, name="deposite_history"),

    path('expenditure/history/', views.expenditure_history, name="expenditure_history"),
    path('expenditure/history/<int:year>/', views.expenditure_history, name="expenditure_history"),
    path('expenditure/history/<int:year>/<int:month>/', views.expenditure_history, name="expenditure_history"),
    path('expenditure/history/<int:year>/<int:month>/<int:day>/', views.expenditure_history, name="expenditure_history"),

    path('deposite/history/', views.deposite_history, name="deposite_history"),
    path('deposite/history/<int:year>/', views.deposite_history, name="deposite_history"),
    path('deposite/history/<int:year>/<int:month>/', views.deposite_history, name="deposite_history"),
    path('deposite/history/<int:year>/<int:month>/<int:day>/', views.deposite_history, name="deposite_history"),



    path('bank/to/cash/', views.bank_to_cash, name="bank_to_cash"),
    path('add_bank/', views.add_bank, name="add_bank"),
    path('add/cash/', views.add_cash, name="add_cash"),

]