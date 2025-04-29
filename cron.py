from apscheduler.schedulers.background import BackgroundScheduler
from main import sendEmail
import pandas as pd
import time 

def scheduled_job():
    try:
        df = pd.read_excel(r"C:\Users\pggoe\OneDrive\ドキュメント\Python_Projects\data.xlsx.xlsx") 
        for index, row in df.iterrows():
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