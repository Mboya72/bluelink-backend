import requests
import base64
from datetime import datetime
from django.conf import settings
from requests.auth import HTTPBasicAuth

class MpesaService:
    @staticmethod
    def get_access_token():
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(
            url, 
            auth=HTTPBasicAuth(settings.MPESA_CONFIG['CONSUMER_KEY'], settings.MPESA_CONFIG['CONSUMER_SECRET'])
        )
        return response.json().get('access_token')

    @staticmethod
    def stk_push(phone, amount, order_id):
        access_token = MpesaService.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            (settings.MPESA_CONFIG['SHORTCODE'] + settings.MPESA_CONFIG['PASSKEY'] + timestamp).encode()
        ).decode()

        payload = {
            "BusinessShortCode": settings.MPESA_CONFIG['SHORTCODE'],
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PhoneNumber": phone,
            "PartyA": phone,
            "PartyB": settings.MPESA_CONFIG['SHORTCODE'],
            "CallBackURL": settings.MPESA_CONFIG['CALLBACK_URL'],
            "AccountReference": f"Order-{order_id}",
            "TransactionDesc": "Payment for Bluelink Order"
        }

        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        response = requests.post(url, json=payload, headers=headers)
        return response.json()