from openpyxl import Workbook

from forms import Questionnaire
from main import write_form_data_to_xlsx, write_questionnaire_to_xlsx
from spreadsheets import get_spreadsheet_data_values, get_spreadsheet_data

# Before launch run pip install -r frozenpip.txt

# Get the id from url
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'

# Spreadsheet worksheet name
RANGE_NAME = 'Form Responses 1'

# Online google form url
FORM_URL = 'YOUR_FORM_URL'

# Getting form data and questionnaire
form_data = get_spreadsheet_data_values(get_spreadsheet_data(SPREADSHEET_ID, RANGE_NAME))
questionnaire = Questionnaire.from_url(FORM_URL)

# Creating a workbook
wb = Workbook()
ws = wb.active
ws.title = RANGE_NAME
# Writing data from spreadsheet to workbook
write_form_data_to_xlsx(ws, form_data, questionnaire)

# Writing questionnaire to workbook
ws = wb.create_sheet('Questionnaire')
write_questionnaire_to_xlsx(ws, questionnaire)

# Saving workbook
wb.save(f'{SPREADSHEET_ID}.xlsx')
print(f'Successfully saved {SPREADSHEET_ID}.xlsx')