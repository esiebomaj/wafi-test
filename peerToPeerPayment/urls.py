from django.urls import path
from peerToPeerPayment import views

urlpatterns = [
    path('add_user/', views.create_user_view, name="add_user"),
    path('deposit/', views.deposit, name="deposit"),
    path('withdraw/', views.withdraw, name="withdraw"),
    path('transfer/', views.transfer, name="transfer"),
    path('check_balance/<str:username>', views.check_balance, name="check_balance"),
]
