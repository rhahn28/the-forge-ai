# main.py
import os
import base64
import schedule
from time import sleep
from openai import OpenAI
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Authenticate and authorize app
if os.path.exists('credentials.json'):
    creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)
else:
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('credentials.json', 'w') as token:
        token.write(creds.to_json())

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to read and draft email responses
def fetch_and_draft_emails():
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], q='is:unread').execute()
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        msg_snippet = msg['snippet']
        thread_id = msg['threadId']

        # Use OpenAI to draft response
        response = openai_client.chat.completions.create(model='text-davinci-003', messages=[{'role': 'system', 'content': 'Draft a response'}, {'role': 'user', 'content': msg_snippet}])
        draft_content = response['choices'][0]['message']['content']

        # Create draft
        message_text = f'To: {msg['payload']['headers']['From']}
From: me
Subject: Re: {msg['payload']['headers']['Subject']}

{draft_content}'
        create_message = {'raw': base64.urlsafe_b64encode(message_text.encode('UTF-8')).decode('ascii')}
        service.users().drafts().create(userId='me', body={'message': create_message}).execute()

# Schedule the job to fetch and draft emails hourly
schedule.every().hour.do(fetch_and_draft_emails)

while True:
    schedule.run_pending()
    sleep(60)
