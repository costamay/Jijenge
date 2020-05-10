from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
import requests
import json
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode
from datetime import datetime

from custom.credentials import credentials, receivePaymentsBillPaymentsSignature, receivePaymentsEazzypayPushSignature, receivePaymentsMerchantPaymentsSignature, JengaAccessToken, receivePaymentsMerchantPaymentsSignature

from .serializer import LipaOnlineSerializer,PayBillSerializer,EasyPaySerializer, CardPaymentSerializer
from payment.models import LipaOnline, PayBill, EasyPay, CardPayment


from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from custom.access_token import generate_access_token
  
# Receiving money

class EasyPayView(viewsets.ModelViewSet):
    queryset = EasyPay.objects.all()
    serializer_class = EasyPaySerializer

    def create(self, request):
        user = request.user
        
        message = "52118221056710937194KE".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        mobileNumber = request.POST.get('mobileNumber') 
        amount = request.POST.get('amount')
        access_token = generate_access_token()
        
        print("ACCESS TOKEN",access_token)
        # api_url = 'https://sandbox.jengahq.io/transaction-test/v2/payments'
        api_url = "https://uat.jengahq.io/transaction/v2/payments"
        headers = {"Authorization": "Bearer %s" % access_token, "signature": signBase64,"Content-Type": "application/json"}
        
        request = {
            "customer": {
                "mobileNumber": mobileNumber,
                "countryCode": "KE"
            },
            "transaction": {
                "amount": amount,
                "description": "A short description",
                "type": "exampleType",
                "reference": "5454512"
            }
        }
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)

class ReceivePaymentsLipanaMPesaOnlineView(viewsets.ModelViewSet):
    queryset = LipaOnline.objects.all()
    serializer_class = LipaOnlineSerializer

    def create(self, request):
        user = request.user
        mobileNumber = request.POST.get('mobileNumber') 
        amount = request.POST.get('amount')
        access_token =generate_access_token()
        
        print("ACCESS TOKEN",access_token)
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



class ReceivePaymentsBillPaymentsView(viewsets.ModelViewSet):
    queryset = PayBill.objects.all()
    serializer_class = PayBillSerializer
    
    def create(self,request):
        user = request.user
        
        message = "3203201111234567291230011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        # url = "https://sandbox.jengahq.io/transaction-test/v2/bills/pay"
        api_url = "https://uat.jengahq.io/transaction/v2/bills/pay"
        access_token = generate_access_token()
        
        mobileNumber = request.POST.get('mobileNumber') 
        amount = request.POST.get('amount')
        
        headers = {
            'Authorization': 'Bearer %s' % access_token,
            'Content-Type': 'application/json',
            'signature': signBase64
        }
        
        request = {
            "biller": {
                "billerCode": "320320",
                "countryCode": "KE"
            },
            "bill": {
                "reference": "101704",
                "amount": amount,
                "currency": "KES"
            },
            "payer": {
                "name": "A. N Other",
                "account": "101704",
                "reference": "123456729123",
                "mobileNumber": mobileNumber
            },
            "partnerId": "0011547896523",
            "remarks": "These are just some remarks"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    
class receivePaymentsMerchantPaymentsView(viewsets.ModelViewSet):
    queryset = PayBill.objects.all()
    serializer_class = PayBillSerializer
    
    def create(self,request):
        message = "076611211200115478965231000KES123456789123".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        # url = receivePaymentsMerchantPaymentsSignature.url
        api_url = "https://uat.jengahq.io/transaction/v2/tills/pay"
        access_token = generate_access_token()
        
        headers = {
            'Authorization': 'Bearer %s' % access_token,
            'Content-Type': 'application/json',
            'signature': signBase64
        }
        
        request = {
            "merchant": {
                "till": "0766112112"
            },
            "payment": {
                "ref": "123456789123",
                "amount": "1000.00",
                "currency": "KES"
            },
            "partner": {
                "id": "0011547896523",
                "ref": "987654321"
            }
        }
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    


class MIGSCardPaymentView(viewsets.ModelViewSet):
    queryset = CardPayment.objects.all()
    serializer_class = CardPaymentSerializer
    
    def create(self, request):
        user = request.user
        mobileNumber = request.POST.get('mobileNumber') 
        amount = request.POST.get('amount')
        cardNumber = request.POST.get("cardNumber")
        # url = "https://sandbox.jengahq.io/transaction-test/v2/migs/payment"
        api_url = "https://uat.jengahq.io/transaction/v2/migs/payment"
        access_token = generate_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            # 'signature': 'vtU9bsRz0WSBrjLYY4dbqloUd0bk7mE6rYa80jxJls7R++YA5hStZIh8mZkMFwQ4UEfXIwQQES8DpP0H9lhyt62ftLf3i6M4WcI31KV4VK2w2Wqf7ZVouw1pYbitWuMcoEQc0YUHBUPMFVmuO8N82ns72914Oms3iOlxg9/pkC1W/FWCHQAOq8RWNGFpmsufEtEnKUOUKAsj0+yVrJ1fpUEpqG2I5hVipz0/c0RVAhuHnTH+/YY6n7jCraSUMMGSfgUDPwY7WgaVfMVv30UTKsq6a0JEdsvOeUVr4jDao+WLK4W6cv3S2vJSDex5lmnQykFptWeVZn0u0PsPu1aTfw=='
        }
        
        request = {
            "transaction": {
                "reference": "23444",
                "orderRef": "8777738",
                "amount": amount,
                "currency": "KES",
                "description": "Test Card Payment",
                "orderExpiry": "2018-08-25T19:00:00",
                "date": "2018-08-27T11:49:58+00:00",
                "postedDate": "2018-08-27T11:49:58",
                "valueDate": "2018-08-27+00:00",
                "billerCode": "900900"
            },
            "card": {
                "number": cardNumber,
                "expiry": "1810",
                "securityCode": "125"
            },
            "customer": {
                "name": "A N Other",
                "customerid": "0000000000",
                "mobileNumber": mobileNumber
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)

def billValidation(request):
    url = "https://sandbox.jengahq.io/transaction-test/v2/bills/validation"
    
    headers = {
        'Authorization': 'Bearer 716iTk7PFteWC8GBGXcOG9l2ZkGr',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "billerCode": "320320",
        "customerRefNumber": "28055948",
        "amount": "1000.00",
        "amountCurrency": "KES"
    }
    
    
    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
    
# sending money

class withinEquity(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "100KES742194625798Tom Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "John Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "bank",
                "countryCode": "KE",
                "name": "Tom Doe",
                "accountNumber": "0060161911111"
            },
            "transfer": {
                "type": "InternalFundsTransfer",
                "amount": "100.00",
                "currencyCode": "KES",
                "reference": "742194625798",
                "date": "2019-05-01",
                "description": "Some remarks here"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
        
class ToMobileWallets(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "20KES692194625798John Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "Tom Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "mobile",
                "countryCode": "KE",
                "name": "John Doe",
                "mobileNumber": "0763555619",
                "walletName": "Equitel"
            },
            "transfer": {
                "type": "MobileWallet",
                "amount": "20",
                "currencyCode": "KES",
                "reference": "692194625798",
                "date": "2019-05-01",
                "description": "Some remarks here"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    
class RTGS(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "4KES692194625798Tom Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "John Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "bank",
                "countryCode": "KE",
                "name": "Tom Doe",
                "bankCode": "70",
                "accountNumber": "12365489"
            },
            "transfer": {
                "type": "RTGS",
                "amount": "4.00",
                "currencyCode": "KES",
                "reference": "692194625798",
                "date": "2019-05-01",
                "description": "Some remarks here"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    
class SWIFT(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "4USD692194625798Tom Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "John Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "bank",
                "countryCode": "JP",
                "name": "Tom Doe",
                "bankBic": "BOTKJPJTXXX",
                "accountNumber": "12365489",
                "addressline1": "Post Box 56"
            },
            "transfer": {
                "type": "SWIFT",
                "amount": "4.00",
                "currencyCode": "USD",
                "reference": "692194625798",
                "date": "2019-05-01",
                "description": "Some remarks here",
                "chargeOption": "SELF"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    
class EFT(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "4KES692194625798Tom Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "John Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "bank",
                "countryCode": "KE",
                "name": "Tom Doe",
                "bankCode": "01",
                "branchCode": "112",
                "accountNumber": "54545"
            },
            "transfer": {
                "type": "EFT",
                "amount": "4.00",
                "currencyCode": "KES",
                "reference": "692194625798",
                "date": "2019-05-01",
                "description": "Some remarks here"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    
class PesalinkToBankAccount(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "4KES692194625798Tom Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "John Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "bank",
                "countryCode": "KE",
                "name": "Tom Doe",
                "bankCode": "63",
                "accountNumber": "0090207635001"
            },
            "transfer": {
                "type": "PesaLink",
                "amount": "4.00",
                "currencyCode": "KES",
                "reference": "692194625798",
                "date": "2019-05-01",
                "description": "Some remarks here"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    
class PesalinkToBankAccount(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        class PesalinkToBankAccount(viewsets.ModelViewSet):
        def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "4KES692194625798Tom Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "John Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "bank",
                "countryCode": "KE",
                "name": "Tom Doe",
                "bankCode": "63",
                "accountNumber": "0090207635001"
            },
            "transfer": {
                "type": "PesaLink",
                "amount": "4.00",
                "currencyCode": "KES",
                "reference": "692194625798",
                "date": "2019-05-01",
                "description": "Some remarks here"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    
class PesalinkToMobileNumber(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://uat.jengahq.io/transaction/v2/remittance"
        access_token = generate_access_token()
        
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "40KES692194625798Tom Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "John Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "mobile",
                "countryCode": "KE",
                "name": "Tom Doe",
                "bankCode": "01",
                "mobileNumber": "0722000000"
            },
            "transfer": {
                "type": "PesaLink",
                "amount": "40.00",
                "currencyCode": "KES",
                "reference": "692194625798",
                "date": "2019-05-01",
                "description": "Some remarks here"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
        # getting signature
        # message = transfer.amount + transfer.currencyCode + transfer.reference + destination.name + source.accountNumber
        message = "40KES692194625798Tom Doe0011547896523".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "source": {
                "countryCode": "KE",
                "name": "John Doe",
                "accountNumber": "0011547896523"
            },
            "destination": {
                "type": "mobile",
                "countryCode": "KE",
                "name": "Tom Doe",
                "bankCode": "01",
                "mobileNumber": "0722000000"
            },
            "transfer": {
                "type": "PesaLink",
                "amount": "40.00",
                "currencyCode": "KES",
                "reference": "692194625798",
                "date": "2019-05-01",
                "description": "Some remarks here"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
    
# Purchase Airtime

class PurchaseAirtime(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        
        
        api_url = "https://api.jengahq.io/transaction/v2/airtime"
        access_token = generate_access_token()
        
        # getting signature
        # message = merchant.code + airtime.telco + airtime.amount + airtime.reference
        message = "6710937194Equitel100692194625798".encode('utf-8') 
        digest = SHA256.new()
        digest.update(message)

        private_key = False
        with open("privatekey.pem", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sigBytes = signer.sign(digest)
        signBase64 = b64encode(sigBytes)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
            'signature': signBase64
        }
        
        request = {
            "customer": {
                "countryCode": "KE",
                "mobileNumber": "0765555131"
            },
            "airtime": {
                "amount": "100",
                "reference": "692194625798",
                "telco": "Equitel"
            }
        }
        
        response = requests.post(api_url, json=request, headers=headers)
        return JsonResponse(response.json(), safe=False)
        
