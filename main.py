from __future__ import print_function

import json
import logging
import os.path
from datetime import datetime
from logging.config import dictConfig

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

MAX_PAGE_SIZE = 1000
FILE_FIELDS = "name, modifiedTime, id, trashed, ownedByMe, md5Checksum"

# For log file naming
date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S%p")

LOGGER_NAME = 'GDrive Duplicate Remover'


def main():
    api_client = get_gdrive_api_client()

    # Call the Drive v3 API to get list of files
    next_page_token = None
    hash_map = {}  # for storing all retrieved files
    while True:
        results = api_client.files().list(
            # Exclude files without md5Checksum
            q="mimeType!='application/vnd.google-apps.folder' and "
              "mimeType!='application/vnd.google-apps.spreadsheet' and "
              "mimeType!='application/vnd.google-apps.presentation' and "
              "mimeType!='application/vnd.google-apps.document' and "
              "mimeType!='application/vnd.google-apps.form' and "
              "mimeType!='application/vnd.google-apps.drive-sdk.810194666617' and "
              "mimeType!='application/vnd.google-apps.site' and "
              "mimeType!='application/vnd.google-apps.earth' and "
              "mimeType!='application/vnd.google-apps.drawing' and "
              "mimeType!='application/vnd.google-apps.jam' and "
              "trashed=false",
            pageSize=MAX_PAGE_SIZE,
            pageToken=next_page_token,
            fields=f"nextPageToken, files({FILE_FIELDS})"
        ).execute()

        next_page_token = results.get('nextPageToken', None)
        logger.info(f'next_page_token: {next_page_token}')
        files = results.get('files', [])
        if not files:
            logger.info('No files found.')
        else:
            for file in files:
                if(file.get('md5Checksum') is not None and
                        file.get('trashed') is False and
                        file.get('ownedByMe') is True):
                    md5_checksum = file['md5Checksum']
                    file_list = hash_map.get(md5_checksum)
                    if file_list is None:
                        hash_map[md5_checksum] = [file]
                    else:
                        file_list.append(file)
        if next_page_token is None:
            break

    logger.info(f'Total number of md5Checksum entries: {len(hash_map)}')

    # Log candidate files to a file
    with open(f'candidate_files-{date}.log', 'w') as log_file:
        for md5_checksum, file_list in hash_map.items():
            log_file.write(md5_checksum + '\n')
            for file in file_list:
                log_file.write(f"\tName: {file['name']} "
                               f"- modifiedTime: {file['modifiedTime']} "
                               f"- ID: {file['id']} "
                               f"- ownedByMe: {file['ownedByMe']} "
                               f"- trashed: {file['trashed']} "
                               f"- md5Checksum: {file['md5Checksum']}\n")

    # Loop through the hash map
    # For each file list under a md5Checksum,
    #   if num of files > 1,
    #   loop through the file list to mark which files to soft delete i.e. trash
    #   loop through the file list again to trash marked files
    to_trash_files_log = open(f'to_trash_files-{date}.log', 'a')
    trashed_files_log = open(f'trashed_files-{date}.log', 'a')
    for md5_checksum, file_list in hash_map.items():
        if len(file_list) > 1:
            # Assuming the first file is the most recent file
            most_recent_file = file_list[0]
            # Loop through the file list to
            #   1) mark trash_mark for each file
            #   2) find out which file is the most recent file
            for file in file_list:
                file['trashed'] = True
                if file['modifiedTime'] > most_recent_file['modifiedTime']:
                    most_recent_file = file
            # Mark trash_mark for the most recent file
            most_recent_file['trashed'] = False
            # Loop through the file list to delete duplicates
            to_trash_files_log.write(md5_checksum + '\n')
            for file in file_list:
                log_str = (f"\tName: {file['name']} "
                           f"- modifiedTime: {file['modifiedTime']} "
                           f"- ID: {file['id']} "
                           f"- ownedByMe: {file['ownedByMe']} "
                           f"- trashed: {file['trashed']} "
                           f"- md5Checksum: {file['md5Checksum']}"
                           f"\n")
                to_trash_files_log.write(log_str)
                if file['trashed'] is True:
                    logger.info(f'Trash file: {file}')
                    trashed_files_log.write(log_str)

                    results = api_client.files().update(fileId=file['id'],
                                                     body={'trashed': True}
                                                     ).execute()
                    logger.info(f'Trash file result: {results}')
    # Close file resources
    to_trash_files_log.close()
    trashed_files_log.close()


def get_gdrive_api_client():
    """This function takes Google Developer App client secrets from a file
    `credentials.json`, kicks off authorization flow, and creates a `service`
    object for Google Drive API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service


if __name__ == '__main__':
    # Config logging
    with open('logging_config.json', 'r') as logging_config_file:
        logging_config = json.load(logging_config_file)
        dictConfig(logging_config)
    logger = logging.getLogger(LOGGER_NAME)

    main()
