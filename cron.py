from apscheduler.schedulers.background import BackgroundScheduler
from main import sendEmail
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from main import sendEmail 

SERVICE_ACCOUNT_FILE = 'C:\Users\pggoe\Downloads\birthday-wisher-460114-8b7520e382cb.json' 
SPREADSHEET_ID = 'pggoel1334@gmail.com'  
RANGE_NAME = 'BirthdayData!Name:Email' 

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def fetch_sheet_data():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print("No data found in Google Sheet.")
        return None

    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def scheduled_job():
    try:
        df = fetch_sheet_data()
        if df is None or df.empty:
            print("No data to process.")
            return

        today = datetime.datetime.now().strftime("%d-%m")
        for index, row in df.iterrows():
            bday = pd.to_datetime(row['Date'], dayfirst=True).strftime("%d-%m")
            if bday == today:
                to = row['Email']
                msg = row['Dialogue']
                subject = "Happy Birthday"
                sendEmail(to, subject, msg)

        print("Birthday emails processed successfully.")
    except Exception as e:
        print(f"Error in scheduled job: {e}")

if __name__ == "__main__":
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(scheduled_job, 'cron', hour=0, minute=0)  # every day at midnight IST
    scheduler.start()

    print("Scheduler started. Waiting for jobs...")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")
