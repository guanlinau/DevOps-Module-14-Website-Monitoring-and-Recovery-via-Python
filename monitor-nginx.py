import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('PASSWORD')

def send_notification (email_msg):
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, PASSWORD)
        message =f"Subject: SITE DOWN!!!\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS,message )

try:
    response = requests.get('http://13.239.111.53:8080')
    if (response.status_code == 200):
        print('Application is running successfully!')
    else:
        print("Application Down. Fix it!")
        # Send email to me
        email_msg = f"Application returned {response.status_code}, should be fixed soon!"
        send_notification(email_msg)
except Exception as ex:
    print(f'Connection error happened:{ex}')
    email_msg="Application not accessible at all!"
    send_notification(email_msg)