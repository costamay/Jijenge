import requests
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import json
from base64 import b64decode, b64encode
from datetime import datetime

class credentials:
    authorization = 'Basic Q25xSlZoNVBkMmFEdEVlSmNhbTRzTzljS0diWWwwWU06M0VwUEdFR3FHUnJLcmhjYQ=='
    password = 'pimW7UAtQTqqwc7gHhnzm4YIECZoud3b'
    username = '6710937194'
    url = "https://uat.jengahq.io/identity/v2/token"
    payload = dict(username=username, password=password)
    
    # mpesa_access_token = json.loads(r.text)
    # validated_mpesa_access_token = mpesa_access_token['access_token']
    # return HttpResponse(validated_mpesa_access_token)
    # payload = 'username=6710937194&password=pimW7UAtQTqqwc7gHhnzm4YIECZoud3b'
    
class JengaAccessToken:
    headers = {
        'authorization': credentials.authorization,
        'content-type': "application/x-www-form-urlencoded"
    }
    
    response = requests.request("POST", credentials.url, data=credentials.payload, headers=headers)
    jenga_access_token = json.loads(response.text)
    validated_jenga_access_token = jenga_access_token['access_token']


    
    
class receivePaymentsBillPaymentsSignature:
    url = "https://sandbox.jengahq.io/transaction-test/v2/bills/pay"
    
    message = "3203201111234567291230011547896523".encode('utf-8') 
    digest = SHA256.new()
    digest.update(message)

    private_key = False
    
    with open("privatekey.pem", "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    signer = PKCS1_v1_5.new(private_key)
    sigBytes = signer.sign(digest)
    signBase64 = b64encode(sigBytes)
    
class receivePaymentsEazzypayPushSignature:
    # url = "https://sandbox.jengahq.io/transaction-test/v2/payments"
    # url = "https://uat.jengahq.io/transaction/v2/payments"
    
    message = "52118221056710937194KE".encode('utf-8') 
    digest = SHA256.new()
    digest.update(message)

    private_key = False
    with open("privatekey.pem", "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    signer = PKCS1_v1_5.new(private_key)
    sigBytes = signer.sign(digest)
    signBase64 = b64encode(sigBytes)
    
class receivePaymentsMerchantPaymentsSignature:
    url = "https://sandbox.jengahq.io/transaction-test/v2/tills/pay"
    
    message = "076611211200115478965231000KES123456789123".encode('utf-8') 
    digest = SHA256.new()
    digest.update(message)

    private_key = False
    with open("privatekey.pem", "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    signer = PKCS1_v1_5.new(private_key)
    sigBytes = signer.sign(digest)
    signBase64 = b64encode(sigBytes)