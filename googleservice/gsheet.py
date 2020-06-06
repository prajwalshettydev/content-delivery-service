from __future__ import print_function
import pickle
import os.path
import typing
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from enum import Enum, unique


@unique
class ValueInputOption(Enum):
    INPUT_VALUE_OPTION_UNSPECIFIED = 1
    RAW = 2
    USER_ENTERED = 3


token_pickle: str
credentials: str
auth_scope: str
service: Resource


def init(token_pickle_loc, sheet_credentials, sheet_auth_scope):
    global token_pickle, credentials, auth_scope, service

    token_pickle = token_pickle_loc
    credentials = sheet_credentials
    auth_scope = sheet_auth_scope

    service = authenticate_to_gsheet()


def authenticate_to_gsheet():  # -> googleapiclient.discovery.Resource:
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials, [auth_scope])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_pickle, 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)

    # &ranges={RANGE_A1} #, includeGridData=True #includeGridData=true&
    # '?fields=sheets%2Fdata%2FrowData%2Fvalues%2FuserEnteredValue'
    # result_sheet = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, includeGridData=True ).execute()


def get_range_from_sheet(sheet_id: str, cell_range: str):
    #service: googleapiclient.discovery.Resource = authenticate_to_gsheet()

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=cell_range,).execute()
    values = result.get('values', [])

    return values


def set_range_of_sheet(sheet_id: str, cell_range: str, body):
    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id, range=cell_range,
        valueInputOption=ValueInputOption.USER_ENTERED.name, body=body).execute()
    return result

def get_particular_row_from_sheet(sheet_id: str, row_index: int):
    service: googleapiclient.discovery.Resource = authenticate_to_gsheet()

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_sheet = sheet.get(spreadsheetId=sheet_id,
                             includeGridData=True).execute()

    data_sheet1 = result_sheet.get('sheets')[0]
    data_row = data_sheet1['data'][0]['rowData'][row_index]['values']

    # Process the row data, and remove unwanted keys
    data_row = [x.get('userEnteredValue') for x in data_row]

    print("\nProcessed list: " + str(data_row) + "\n")

    return data_row
