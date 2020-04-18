import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
TOKEN_CACHE_FILE = 'token.pickle'

CREDS_GET_URL = 'https://console.developers.google.com/henhouse/?pb=%5B%22hh-0%22%2C%22sheets.googleapis.com%22%2Cnull%2C%5B%5D%2C%22https%3A%2F%2Fdevelopers.google.com%22%2Cnull%2C%5B%5D%2Cnull%2C%22Enable%20the%20Google%20Sheets%20API%22%2C1%2Cnull%2C%5B%5D%2Cfalse%2Cfalse%2Cnull%2Cnull%2Cnull%2Cnull%2Cfalse%2Cnull%2Cfalse%2Cfalse%2Cnull%2Cnull%2Cnull%2C%22DESKTOP%22%2Cnull%2C%22Gforms%22%2Ctrue%2C%22Gforms%22%2Cnull%2Cnull%2Cfalse%5D'
CREDS_FILE_NAME = 'credentials.json'


def get_spreadsheet_data(spreadsheet_id, sheet_range):
	"""Shows basic usage of the Sheets API.
	Prints values from a sample spreadsheet.
	"""
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists(TOKEN_CACHE_FILE):
		with open(TOKEN_CACHE_FILE, 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:

			try:
				flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE_NAME, SCOPES)
			except FileNotFoundError as e:
				raise Exception(f'File {CREDS_FILE_NAME} not found. Obtain it by enabling spreadsheet API at:\n{CREDS_GET_URL}')
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open(TOKEN_CACHE_FILE, 'wb') as token:
			pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)

	# Call the Sheets API
	sheet = service.spreadsheets()
	return sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_range).execute()


def get_spreadsheet_data_values(spreadsheet_data):
	try:
		return spreadsheet_data['values']
	except KeyError:
		print('No data found.')
		return [[]]
