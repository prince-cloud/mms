from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'finance'


urlpatterns = [
    path("", views.index, name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('add_expenditure/', views.add_expenditure, name="add_expenditure"),
    path('deposite/', views.deposite, name="deposite"),
    path('approve_deposite/<int:pk>/', views.approve_deposite, name="approve_deposite"),
    path('approvals/', views.approvals, name="approvals"),
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

]