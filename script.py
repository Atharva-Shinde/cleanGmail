import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def create_service():
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    #         creds = flow.run_local_server(port=0)
    #         with open("token.json", "w") as token:
    #             token.write(creds.to_json())
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

def get_messages(service):
    data = service.users().messages().list(userId='me',maxResults=500).execute()
    messages = data.get('messages',[])
    message_ids =[]
    for message in messages:
        message_ids.append(message['id'])
    return message_ids

def get_starred(service):
    data = service.users().messages().list(userId='me', labelIds=['STARRED'],maxResults=200).execute()
    starred_messages = data.get('messages',[])
    starred_ids = []
    for message_data in starred_messages:
        starred_ids.append(message_data['id'])
    return starred_ids

def main():
    service = create_service()
    ids = get_messages(service)
    if len(ids)==0:
        return
    star_ids = get_starred(service)

if __name__ == "__main__":
  main()