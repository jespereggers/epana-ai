import requests
import json

def initiate_paypal_payment(amount, currency, description):
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    base_url = 'YOUR_BASE_URL'

    # Get access token
    auth_url = f'{base_url}/v1/oauth2/token'
    auth_headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_response = requests.post(auth_url, auth=(client_id, client_secret), data=auth_data, headers=auth_headers)
    access_token = auth_response.json()['access_token']

    # Create payment
    payment_url = f'{base_url}/v2/checkout/orders'
    payment_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    payment_data = {
        'intent': 'CAPTURE',
        'purchase_units': [{
            'amount': {
                'currency_code': currency,
                'value': amount
            },
            'description': description
        }]
    }
    payment_response = requests.post(payment_url, json=payment_data, headers=payment_headers)

    if payment_response.status_code == 201:
        payment_id = payment_response.json()['id']
        return payment_id
    else:
        print('Failed to create payment:')
        print(payment_response.json())
        return None

# Example usage
amount = '10.00'
currency = 'USD'
description = 'Test Payment'
payment_id = initiate_paypal_payment(amount, currency, description)
if payment_id:
    print(f'Payment initiated successfully. Payment ID: {payment_id}')
else:
    print('Payment initiation failed.')
