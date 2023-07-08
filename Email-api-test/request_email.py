import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Set up credentials
credentials = Credentials.from_authorized_user_file('credentials.json', ['https://www.googleapis.com/auth/gmail.readonly'])
service = build('gmail', 'v1', credentials=credentials)

# Retrieve emails
results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
messages = results.get('messages', [])

# Iterate over messages
for message in messages:
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    email_data = msg['payload']['headers']

    # Extract email information
    for values in email_data:
        name = values['name']
        if name == 'From':
            from_name = values['value']
        elif name == 'To':
            to_name = values['value']
        elif name == 'Subject':
            subject = values['value']
        elif name == 'Date':
            date = values['value']

    # Extract email body
    if 'parts' in msg['payload']:
        parts = msg['payload']['parts']
        data = parts[0]['body']["data"]
    else:
        data = msg['payload']['body']["data"]

    # Decode and print email details
    raw_data = base64.urlsafe_b64decode(data).decode('utf-8')
    print('From:', from_name)
    print('To:', to_name)
    print('Subject:', subject)
    print('Date:', date)
    print('Body:', raw_data)
    print('------------------------------------')
