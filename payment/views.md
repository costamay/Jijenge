from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
import requests
import json
from . credentials import credentials, receivePaymentsBillPaymentsSignature, receivePaymentsEazzypayPushSignature, receivePaymentsMerchantPaymentsSignature, JengaAccessToken, receivePaymentsMerchantPaymentsSignature

from .serializer import LipaOnlineSerializer, EazzyPaySerializer
from payment.models import LipaOnline


from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


def getJengaToken(request):
    # url = "https://sandbox.jengahq.io/identity-test/v2/token"
    url = "https://uat.jengahq.io/identity/v2/token"
    # url = "https://api-test.equitybankgroup.com/v1/token"
    

    # payload = "grant_type=password&merchantCode=6710937194&password=pimW7UAtQTqqwc7gHhnzm4YIECZoud3b"
    # payload = 'username=6710937194&password=pimW7UAtQTqqwc7gHhnzm4YIECZoud3b'
    payload = dict(username=credentials.username, password=credentials.password)
    headers = {
        'authorization': credentials.authorization,
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    print('rrrrrrrrrrrrr')
    print(response.text.encode('utf8'))
    print('rrrrrrrrrrrrr')
    jenga_access_token = json.loads(response.text)
    print(jenga_access_token)
    print('rrrrrrrrrrrrr')
    validated_jenga_access_token = jenga_access_token['access_token']
    return HttpResponse(validated_jenga_access_token)
    
    
    
class ReceivePaymentsLipanaMPesaOnlineView(viewsets.ModelViewSet):
    queryset = LipaOnline.objects.all()
    serializer_class = LipaOnlineSerializer

    def create(self, request):
        user = request.user
        mobileNumber = request.POST.get('mobileNumber')
        amount = request.POST.get('amount')
        access_token = JengaAccessToken.validated_jenga_access_token
        api_url = "https://uat.jengahq.io/transaction/v2/payment/mpesastkpush"
        headers = {"Authorization": "Bearer %s" % access_token,"Content-Type": "application/json"}
        
        request = {
        "customer": {
            "mobileNumber": mobileNumber,
            "countryCode": "KE"
        },
        "transaction": {
            "amount": amount,
            "description": "A short description",
            "businessNumber": "174379",
            "type": "exampleType",
            "reference": "5211822"
            }
        }
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)

 