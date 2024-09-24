import requests
import json
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
import os

# Load environment variables
load_dotenv()

# Microsoft Azure App Registration details
client_id = os.getenv("CLIENT_ID")
tenant_id = os.getenv("TENANT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Endpoint for OAuth 2.0 token request
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

# Mail sending endpoint
send_mail_url = 'https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail'

# Request body for the token request
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
}

# Request headers for token request
token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Step 1: Obtain access token
token_response = requests.post(token_url, data=token_data, headers=token_headers)
token = token_response.json().get('access_token')

if not token:
    print("Error obtaining access token:", token_response.json())
else:
    print("Access token successfully obtained.")

    # Step 2: Construct the email message
    email_message = {
        "message": {
            "subject": "Microsoft Graph API Test Email",
            "body": {
                "contentType": "Text",
                "content": "Hi, this is a test email sent via the Microsoft Graph API."
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": "weyousathwik@gmail.com"
                    }
                }
            ]
        }
    }

    # Step 3: Set headers and send the email
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Use your valid sender email registered in Azure tenant
    sender_email = '11c3a3bbb051566b' # Must be part of Azure AD

    send_mail_response = requests.post(
        send_mail_url.format(sender_email=sender_email),
        headers=headers,
        json=email_message
    )

    if send_mail_response.status_code == 202:
        print("Email sent successfully.")
    else:
        print(f"Error sending email: {send_mail_response.status_code}")
        print(send_mail_response.json())

