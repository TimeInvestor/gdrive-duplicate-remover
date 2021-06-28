from __future__ import print_function

import json
import logging
import os
from datetime import datetime
from logging.config import dictConfig

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

MAX_PAGE_SIZE = 1000
FILE_FIELDS = "name, modifiedTime, id, trashed, ownedByMe, md5Checksum"

# For reporting
date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S%p")
REPORT_FOLDER = 'reports'

LOGGER_NAME = 'GDrive Duplicate Remover'

# New fields for status tracking of files.
# We can leverage the existing `trashed` field of files, but it may not be a
# good idea as we don't have the control of the field and Google could rename
# or remove the field one day.
# Another benefit of adding new fields, except having control, is it helps
# auditing/failure analysis by have different status field.
TO_REMOVE = 'to_remove'
REMOVED = 'removed'


def main():
    api_client = get_gdrive_api_client()

    hash_map = fetch_files_from_gdrive(api_client)
    logger.info(f'Total number of md5Checksum entries: {len(hash_map)}')
    _produce_candidate_files_report(hash_map)

    _mark_duplicates(hash_map)
    _produce_files_for_removal_report(hash_map)

    remove_duplicates_from_gdrive(api_client, hash_map)
    _produce_files_removed_report(hash_map)


def get_gdrive_api_client():
    """Takes Google Developer App client secrets from a file
    `credentials.json`, kicks off authorization flow, and creates a `service`
    object for Google Drive API.

    Returns:
        A client for Google Drive ready to make calls.
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


def fetch_files_from_gdrive(api_client):
    """Fetches list of files from Google Drive.

    Fetches only files that have md5Checksum. Files that does not have
    md5checksum: folders, Google Docs, Google Sheets, Google Slides,
    and other Google Office files. It also excludes files that are not owned
    by the user or have already been trashed.

    Args:
        api_client: Google Drive API client.

    Returns:
        A dict using files' md5Checksum as the keys. The value for each key
        is a list of files with same md5Checksum i.e. duplicate files.
    """
    hash_map = {}
    next_page_token = None
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
            logger.info('No suitable files found in your Google Drive.')
        else:
            for file in files:
                if (file.get('md5Checksum') is not None and
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

    return hash_map


def remove_duplicates_from_gdrive(api_client, hash_map):
    """Remove duplicate files from Google Drive.

    It actually trash duplicate files by updating a duplicate file's metadata
    field `trashed` to be true.

    Args:
        api_client: Google Drive API client.
        hash_map: a dict contains info about md5Checksum and its related files

    Returns:
        None
    """
    for file_list in hash_map.values():
        for file in file_list:
            if file.get(TO_REMOVE) is True:
                logger.info(f'Trashing file: {file}')
                try:
                    result = api_client.files().update(fileId=file['id'],
                                                       body={'trashed': True}
                                                       ).execute()
                except HttpError:
                    logger.exception('Trashing file failed!')
                else:
                    logger.info(f'Trashing file done - response: {result}')
                    file[REMOVED] = True


def _mark_duplicates(hash_map):
    for md5_checksum, file_list in hash_map.items():
        # Loop through the file list to
        # 1) mark files to be removed
        # 2) find out most recent file to keep
        if len(file_list) > 1:
            most_recent_file = file_list[0]
            for file in file_list:
                file[TO_REMOVE] = True
                if file['modifiedTime'] > most_recent_file['modifiedTime']:
                    most_recent_file = file
            most_recent_file[TO_REMOVE] = False


def _produce_candidate_files_report(hash_map):
    report_file = os.path.join(REPORT_FOLDER, f'Candidate_Files-{date}.log')
    _produce_report(hash_map, report_file)


def _produce_files_for_removal_report(hash_map):
    new_hash_map = {}
    for md5_checksum, file_list in hash_map.items():
        new_list = [file for file in file_list if file.get(TO_REMOVE) is True]
        if len(new_list) > 0:
            new_hash_map[md5_checksum] = new_list

    report_file = os.path.join(REPORT_FOLDER, f'Files_To_Remove-{date}.log')
    _produce_report(new_hash_map, report_file)


def _produce_files_removed_report(hash_map):
    new_hash_map = {}
    for md5_checksum, file_list in hash_map.items():
        new_list = [file for file in file_list if file.get(REMOVED) is True]
        if len(new_list) > 0:
            new_hash_map[md5_checksum] = new_list

    report_file = os.path.join(REPORT_FOLDER, f'Files_Removed-{date}.log')
    _produce_report(new_hash_map, report_file)


def _produce_report(hash_map, report_file):
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, 'w') as f:
        for md5_checksum, file_list in hash_map.items():
            f.write(f"md5Checksum: {md5_checksum}\n")
            for file in file_list:
                f.write(f"\tName: {file['name']} "
                        f"- modifiedTime: {file['modifiedTime']} "
                        f"- ID: {file['id']} "
                        f"- ownedByMe: {file['ownedByMe']} "
                        f"- trashed: {file['trashed']} "
                        f"- md5Checksum: {file['md5Checksum']}\n")


if __name__ == '__main__':
    # Config logging
    with open('logging_config.json', 'r') as logging_config_file:
        logging_config = json.load(logging_config_file)
        dictConfig(logging_config)
    logger = logging.getLogger(LOGGER_NAME)

    # Run the application
    main()
