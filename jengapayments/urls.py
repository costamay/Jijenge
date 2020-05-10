
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers

from jenga_api.views import ReceivePaymentsLipanaMPesaOnlineView, EasyPayView, ReceivePaymentsBillPaymentsView, MIGSCardPaymentView

router = routers.DefaultRouter()
router.register('api/lipaOnline', ReceivePaymentsLipanaMPesaOnlineView),
router.register('api/eazzyPay', EasyPayView),
router.register('api/paybill', ReceivePaymentsBillPaymentsView),
router.register('api/cardpayment', MIGSCardPaymentView)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
    
]

