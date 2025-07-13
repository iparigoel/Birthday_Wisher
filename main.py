import os
from dotenv import load_dotenv
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText

load_dotenv()

GMAIL_ID = os.getenv("EMAIL_ADDRESS")
GMAIL_PSWD = os.getenv("GMAIL_APP_PASSWORD")

def sendEmail(to, sub, msg):
    print(f"Email to {to} sent with subject: {sub} and message {msg}")
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(GMAIL_ID, GMAIL_PSWD)
        s.sendmail(GMAIL_ID, to, f"Subject: {sub}\n\n{msg}")
        
        s.quit()
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email to {to}: {e}")

# if __name__ == "__main__":
#     df = pd.read_excel("data.xlsx.xlsx")
#     # print(df)
#     today = datetime.datetime.now().strftime("%d-%m")
#     yearNow = datetime.datetime.now().strftime("%Y")
#     writeInd = []
#     for index, item in df.iterrows():
#         bday = item['Birthday'].strftime("%d-%m")
#         if(bday == today) and yearNow not in str(item['Year']):
#             sendEmail(item['Email'], "Happy Birthday", item['Dialogue'])
#             writeInd.append(index)

#     if(len(writeInd) != 0):
#         for i in writeInd:
#             yr = df.loc[i, 'Year']
#             df.loc[i, 'Year'] = str(yr) + ',' + str(yearNow)
#         df.to_excel('data.xlsx.xlsx', index = False)