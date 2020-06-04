from __future__ import print_function
import pickle
import os.path
import typing
import config
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
#SPREADSHEET_ID = config.ContentSheet  # config.tweet_sheet
SAMPLE_RANGE_NAME = 'Sheet1!A2:E3'


def authenticate_to_gsheet():  # -> googleapiclient.discovery.Resource:
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(config.token_pickle):
        with open(config.token_pickle, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.sheet_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(config.token_pickle, 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)

    # &ranges={RANGE_A1} #, includeGridData=True #includeGridData=true&
    # '?fields=sheets%2Fdata%2FrowData%2Fvalues%2FuserEnteredValue'
    # result_sheet = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, includeGridData=True ).execute()

    # print("get sheet" + str(result_sheet))
    # values = result.get('values', [])
    # print("\n\n\n\nget sheet values" + str(values))

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    # for row in values:
    # Print columns A and E, which correspond to indices 0 and 4.
    # print('%s, %s' % (row[0], row[1]))  # Prints an entire row


def get_all_cells_from_sheet():
    service: googleapiclient.discovery.Resource = authenticate_to_gsheet()

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=config.ContentSheet,
                                ).execute()  # range=SAMPLE_RANGE_NAME,
    pass


def get_particular_row_from_sheet(row_index: int):
    service: googleapiclient.discovery.Resource = authenticate_to_gsheet()

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_sheet = sheet.get(spreadsheetId=config.ContentSheet,
                             includeGridData=True).execute()

    data_sheet1 = result_sheet.get('sheets')[0]
    data_row = data_sheet1['data'][0]['rowData'][row_index]['values']

    # Process the row data, and remove unwanted keys
    data_row = [x.get('userEnteredValue') for x in data_row]

    print("\nprocessed list: " + str(data_row) + "\n")

    return data_row


if __name__ == '__main__':
    get_particular_row_from_sheet(1)
    pass
    # main()
