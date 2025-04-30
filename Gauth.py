import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def authenticate_gworkspace(scopes, credentials_file='credentials.json'):
    """
    Authenticates with Google Workspace using a service account.

    Args:
        scopes (list): A list of Google API scopes required for accessing data.
                       Example: ['https://www.googleapis.com/auth/drive.file']
        credentials_file (str, optional): Path to the service account credentials JSON file.
                                           Defaults to 'credentials.json'.

    Returns:
        googleapiclient.discovery.Resource: A service object that can be used to
                                             interact with the Google Workspace API,
                                             or None if authentication fails.
    """
    try:
        creds = Credentials.from_service_account_file(
            credentials_file, scopes=scopes)
        service = build('drive', 'v3', credentials=creds)  # Example for Google Drive
        print("Successfully authenticated with Google Workspace.")
        return service
    except Exception as e:
        print(f"Authentication with Google Workspace failed: {e}")
        print(f"Make sure the credentials file '{credentials_file}' exists and is valid.")
        print("Also, ensure the service account has the necessary permissions and the required APIs are enabled.")
        return None

if __name__ == '__main__':
    # Define the required scopes for the Google Workspace service you want to access.
    # For example, to save data to Google Drive, you might need:
    # - 'https://www.googleapis.com/auth/drive.file' (for file access)
    # - 'https://www.googleapis.com/auth/spreadsheets' (for Google Sheets)
    # Consult the specific Google Workspace API documentation for the correct scopes.
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    # Ensure your service account credentials JSON file is in the same directory
    # as your Python script, or provide the correct path to the file.
    CREDENTIALS_FILE = 'path/to/your/credentials.json'  # Replace with the actual path if needed

    # Authenticate with Google Workspace
    drive_service = authenticate_gworkspace(SCOPES, CREDENTIALS_FILE)

    # If authentication was successful, you can now use the 'drive_service' object
    # to interact with the Google Drive API.
    if drive_service:
        # Example: List the first 10 files in your Google Drive
        try:
            results = drive_service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print(f"{item['name']} ({item['id']})")
        except Exception as error:
            print(f'An error occurred: {error}')
