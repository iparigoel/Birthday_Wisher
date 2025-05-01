from apscheduler.schedulers.background import BackgroundScheduler
from main import sendEmail
import pandas as pd
import datetime
import time, os

def scheduled_job():
    try:
        # Get the absolute path to the current file's directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data.csv")

        df = pd.read_csv(file_path)
        today = datetime.datetime.now().strftime("%d-%m")
        for index, row in df.iterrows():
            bday = pd.to_datetime(row['Date'], dayfirst=True).strftime("%d-%m")
            if bday == today:
                to = row['Email']
                msg = row['Dialogue']
                subject = "Happy Birthday"
                sendEmail(to, subject, msg)

        print("Emails sent successfully.")
    except Exception as e:
        print(f"Error sending emails: {e}")

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(scheduled_job, 'cron', hour=00, minute=00)  
scheduler.start()

print("Scheduler started...")

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")