import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


class GoogleSheetsService:
    def __init__(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scope
        )
        self.client = gspread.authorize(creds)

    def read_sheet(self, sheet_name):
        sheet = self.client.open(sheet_name).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        # Clean weird characters
        df = df.replace("â€“", None)
        df = df.replace("", None)

        return df
        
    def update_cell_by_id(self, sheet_name, id_column, row_id, update_column, value):
        sheet = self.client.open(sheet_name).sheet1
        records = sheet.get_all_records()

        for idx, record in enumerate(records, start=2):  # start=2 because row 1 is header
            if record[id_column] == row_id:
                col_index = sheet.find(update_column).col
                sheet.update_cell(idx, col_index, value)
                return True

        return False
    
    