import json
import requests
from requests.auth import HTTPBasicAuth


from custom import keys

def generate_access_token():  
    url = "https://uat.jengahq.io/identity/v2/token"
    payload = dict(username=keys.username, password=keys.password)
    headers = {
        'authorization': keys.authorization,
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    print(response.text.encode('utf8'))
    jenga_access_token = json.loads(response.text)
    print(jenga_access_token)
    validated_jenga_access_token = jenga_access_token['access_token']
    print("VALIDATE tIME",validated_jenga_access_token)
    
    return validated_jenga_access_token