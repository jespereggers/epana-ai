import requests
import json

CLIENT_ID = "AY9rlr3YXt8s5V6rg8m2GAWmT81jbMsPjVcuQV9Q6QMrijtbgLT00uy12i9T91hfQ_2yBv-KZBqH8V0Z"
CLIENT_SECRET = "EP3kAeANsKggWylQYgzwAn-HwLLgEafKKL6V3K8OOD7PGER0bnOQm_Qyv0vhu34-gK3NpE20tv6dvHAc"
BASE_URL = "http://127.0.0.1:5000/"

def initiate_paypal_payment(price, currency, description):
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    base_url = BASE_URL

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
                'value': price
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
payment_id = initiate_paypal_payment("1", "USD", "Epana Mind Upload")
if payment_id:
    print(f'Payment initiated successfully. Payment ID: {payment_id}')
else:
    print('Payment initiation failed.')
