from __future__ import print_function
import os.path
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Retrieves the sender, subject, date, and time of emails from today.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        
        # Calculate the date range
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        query = f"after:{today} before:{tomorrow}"
        
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return
        print('Emails from today:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            headers = msg['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '')
            from_name = next((header['value'] for header in headers if header['name'] == 'From'), '')
            date = next((header['value'] for header in headers if header['name'] == 'Date'), '')
            
            print('From:', from_name)
            print('Subject:', subject)
            print('Date:', date)
            print('------------------------------------')

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
