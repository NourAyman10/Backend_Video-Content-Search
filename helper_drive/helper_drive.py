import re
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "helper_drive/service_account.json"
PARENT_FOLDER_ID = "1iryPHmHRC2eeToIh6EnNt4oq24huNzc5"
OUTPUT_FILE_NAME = 'output'


def get_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)
    return service


def upload_video(file_path):
    service = get_service()

    file_metadata = {"name": OUTPUT_FILE_NAME, "parents": [PARENT_FOLDER_ID]}

    file = service.files().create(body=file_metadata, media_body=file_path).execute()    


def convert_to_preview_link(original_link):
    pattern = r"https://drive.google.com/file/d/([^/]+)/view\?usp=drivesdk"
    preview_link = re.sub(pattern, r"https://drive.google.com/file/d/\1/preview", original_link)
    
    return preview_link


def get_embeddable_link(folder_id, file_name):
    service = get_service()
    
    query = f"'{folder_id}' in parents and name = '{file_name}' and mimeType contains 'video/'"
    response = service.files().list(q=query, fields='files(webViewLink)').execute()
    files = response.get('files', [])
    if files:
        file = files[0]['webViewLink']
        preview_link = convert_to_preview_link(file)
        return preview_link
    else:
        print("Video not found.")
        return None

    
def delete_video(folder_id, file_name):
    service = get_service()
    
    query = f"'{folder_id}' in parents and name = '{file_name}' and mimeType contains 'video/'"
    response = service.files().list(q=query, fields='files(id)').execute()
    files = response.get('files', [])
    if files:
        file_id = files[0]['id']
        service.files().delete(fileId=file_id).execute()
        print("Video deleted successfully.")
    else:
        print("Video not found.")
        

def get_preview_link(file_path):
    folder_id = PARENT_FOLDER_ID
    file_name = 'output'
    
    delete_video(folder_id, file_name)
    upload_video(file_path)
    preview_link = get_embeddable_link(folder_id, file_name)
    return preview_link
