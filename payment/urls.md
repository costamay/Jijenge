from django.urls import path

from . import views

urlpatterns = [
    path('jenga2/token', views.getJengaToken, name='access_token'),
    path('online/lipa', views.receivePaymentsLipanaMPesaOnline, name='lipa_na_mpesa'),
    path('jenga/billpayment', views.receivePaymentsBillPayments, name='billpayment'),
    path('jenga/eazzypush', views.receivePaymentsEazzypayPush, name='eazzypush'),
    path('jenga/merchantpayment', views.receivePaymentsMerchantPayments, name='merchantpayment'),
    
]