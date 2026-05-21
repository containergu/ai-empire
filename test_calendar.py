import json, os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']
creds_file = r'C:\Users\robin\OneDrive\Desktop\George Learning AI\Cursor Claude\client_secret_463094204264-1gsvd3q0dvgnhc0vblu4ni1jo3j4v33g.apps.googleusercontent.com.json'
token_file = os.path.expanduser(r'~\.config\google-calendar-mcp\tokens.json')

creds = None
if os.path.exists(token_file):
    with open(token_file) as f:
        token_data = json.load(f)
        if 'token' in token_data:
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
        creds = flow.run_local_server(port=0)

service = build('calendar', 'v3', credentials=creds)
events_result = service.events().list(
    calendarId='primary',
    timeMin='2026-05-20T00:00:00-07:00',
    timeMax='2026-05-21T00:00:00-07:00',
    singleEvents=True,
    orderBy='startTime'
).execute()
events = events_result.get('items', [])

if not events:
    print('No events found for today.')
else:
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(f'{start} -> {end}')
        print(f'  {event["summary"]}')
        if event.get('location'):
            print(f'  Location: {event["location"]}')
        print()
