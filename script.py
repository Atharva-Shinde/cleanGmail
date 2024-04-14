import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials


def create_service():
    SCOPES = ["https://mail.google.com/"]
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json",SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json",SCOPES)
        creds= flow.run_local_server(port=0)
        with open("token.json","w") as token:
            token.write(creds.to_json())
    service = build("gmail","v1",credentials=creds)
    return service