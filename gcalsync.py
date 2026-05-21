import json, os, sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds_file = r'C:\Users\robin\OneDrive\Desktop\George Learning AI\Cursor Claude\client_secret_463094204264-1gsvd3q0dvgnhc0vblu4ni1jo3j4v33g.apps.googleusercontent.com.json'
token_file = os.path.expanduser(r'~\.config\google-calendar-mcp\tokens.json')

creds = None
# Load client info from credentials file
with open(creds_file) as f:
    client_info = json.load(f).get('installed', {})

if os.path.exists(token_file):
    with open(token_file) as f:
        token_data = json.load(f)
    acct = token_data.get('normal', token_data)
    if acct.get('access_token'):
        creds = Credentials(
            token=acct['access_token'],
            refresh_token=acct.get('refresh_token'),
            token_uri=client_info.get('token_uri', 'https://oauth2.googleapis.com/token'),
            client_id=client_info['client_id'],
            client_secret=client_info['client_secret'],
            scopes=SCOPES
        )

# Refresh or re-auth if needed
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token back
        token_data['normal'] = {
            'access_token': creds.token,
            'refresh_token': creds.refresh_token,
            'scope': ' '.join(creds.scopes),
            'token_type': 'Bearer',
            'expiry_date': creds.expiry.timestamp() * 1000 if creds.expiry else 0
        }
        with open(token_file, 'w') as f:
            json.dump(token_data, f, indent=2)
        print('Token refreshed and saved to MCP token store.')
    else:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
        creds = flow.run_local_server(port=0)

service = build('calendar', 'v3', credentials=creds)
action = sys.argv[1] if len(sys.argv) > 1 else 'list'

if action == 'ls':
    import datetime
    today = datetime.date.today()
    events_result = service.events().list(
        calendarId='primary',
        timeMin=f'{today}T00:00:00-07:00',
        timeMax=f'{today}T23:59:00-07:00',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    for e in events_result.get('items', []):
        s = e['start'].get('dateTime', e['start'].get('date'))
        print(f'{s}  {e["summary"]}')
    if not events_result.get('items'):
        print('No events today.')

elif action == 'add':
    title = sys.argv[2]; date = sys.argv[3]; st = sys.argv[4]; et = sys.argv[5]
    loc = sys.argv[6] if len(sys.argv) > 6 else ''
    desc = sys.argv[7] if len(sys.argv) > 7 else ''
    event = {
        'summary': title,
        'location': loc,
        'description': desc,
        'start': {'dateTime': f'{date}T{st}:00-07:00', 'timeZone': 'America/Los_Angeles'},
        'end': {'dateTime': f'{date}T{et}:00-07:00', 'timeZone': 'America/Los_Angeles'},
    }
    r = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Created: {r.get("htmlLink")}')

print('Done')
