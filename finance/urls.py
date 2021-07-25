from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'finance'


urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('edit-profile/<int:pk>/', views.edit_account, name="edit_account"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('add_expenditure/', views.add_expenditure, name="add_expenditure"),
    path('history/', views.history, name="history"),
    path('expenditure/history/', views.expenditure_history, name="expenditure_history"),

    #expenditure history
    path('expenditure/history/', views.expenditure_history, name="expenditure_history"),
    path('expenditure/history/<int:year>/', views.expenditure_history, name="expenditure_history"),
    path('expenditure/history/<int:year>/<int:month>/', views.expenditure_history, name="expenditure_history"),
    path('expenditure/history/<int:year>/<int:month>/<int:day>/', views.expenditure_history, name="expenditure_history"),

    #cash history
    path('cash/history/', views.cash_history, name="cash_history"),
    path('cash/history/<int:year>/', views.cash_history, name="cash_history"),
    path('cash/history/<int:year>/<int:month>/', views.cash_history, name="cash_history"),
    path('cash/history/<int:year>/<int:month>/<int:day>/', views.cash_history, name="cash_history"),

    #momo history
    path('momo/history/', views.momo_history, name="momo_history"),
    path('momo/history/<int:year>/', views.momo_history, name="momo_history"),
    path('momo/history/<int:year>/<int:month>/', views.momo_history, name="momo_history"),
    path('momo/history/<int:year>/<int:month>/<int:day>/', views.momo_history, name="momo_history"),

    #momo_to_cash_history
    path('momo-cash/history/', views.momo_to_cash_history, name="momo_to_cash_history"),
    path('momo-cash/history/<int:year>/', views.momo_to_cash_history, name="momo_to_cash_history"),
    path('momo-cash/history/<int:year>/<int:month>/', views.momo_to_cash_history, name="momo_to_cash_history"),
    path('momo-cash/history/<int:year>/<int:month>/<int:day>/', views.momo_to_cash_history, name="momo_to_cash_history"),

    path('momo/to/cash/', views.momo_to_cash, name="momo_to_cash"),
    path('add_momo/', views.add_momo, name="add_momo"),
    path('add/cash/', views.add_cash, name="add_cash"),

]