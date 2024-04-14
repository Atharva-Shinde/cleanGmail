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

def get_sent(service):
    data = service.users().messages().list(userId='me',labelIds=['SENT'],maxResults=1000).execute()
    sent_messages = data.get('messages',[])
    sent_message_ids =[]
    for message in sent_messages:
        sent_message_ids.append(message['id'])
    return sent_message_ids

# def get_trashed(service):
#     data = service.users().messages().list(userId='me',labelIds=['TRASH'],maxResults=2000).execute()
#     trash_messages = data.get('messages',[])
#     trash_message_ids =[]
#     for message in trash_messages:
#         # x = service.users().messages().get(userId='me',id=message['id']).execute()
#         # print(x['snippet'])
#         trash_message_ids.append(message['id'])
#     return trash_message_ids

def skim(service,skim_ids,ids):
    for skim_id in skim_ids:
        if skim_id in ids:
            # message = service.users().messages().get(userId='me',id=skim_id).execute()
            # print(message['snippet'])
            ids.remove(skim_id)

def main():
    service = create_service()
    ids = get_messages(service)
    if len(ids)==0:
        return
    star_ids = get_starred(service)
    sent_ids = get_sent(service)
    # trash_ids= get_trashed(service)
    skim_ids = star_ids+sent_ids #+trash_ids
    skim(service,skim_ids,ids)
    # final_ids = ids[::-1]
    with open("log.txt","a") as log:
        for id in ids:
            trash = service.users().messages().trash(userId='me',id=id).execute()
            log.write(str(trash)+"\n")
            print(trash)

if __name__ == "__main__":
  main()