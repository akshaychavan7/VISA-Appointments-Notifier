'''
How to run this script - 
1. Get your sender email ID's password using two-step verification. (Follow this tutorial)
2. Add the Sender Email, Sender Email's Password, and Receiver Email in this script
3. Update the visa_notifier.bat file given in this folder as per your script's path
4. Create a Windows Scheduler Task, so that it will continuously run this script using following steps - 
    i. Search task scheduler in your windows search menu
    ii. Actions -> Create task -> give the name you want for this task
    iii. Open Triggers tab -> Select Daily -> select start date and time as per your current date -> recur every 1 days -> Check repeat task every option and select option as 5 minutes -> OK
    iv. Open Actions tab -> New -> Click on browse -> Select the visa_notifier.bat file that we have created -> OK
    v. To test this task -> right click on the task that you've just created -> run -> it will open a command promt window -> check for the output there
5. Check each day if your script is running or not, this is to avoid any failures.
'''


import os
from email.message import EmailMessage
import ssl
import smtplib


def send_email():
    email_sender = '<YOUR SENDER EMAIL>'
    email_password = '<PASSWORD GENERATED AS MENTIONED IN STEP 1>'
    email_receiver = '<EMAIL WHERE NOTIFICATION NEEDS TO BE SENT>'

    subject = 'VISA Appointmets Available!'
    body = ''

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

######################## WINDOWS NOTIFICATION ##################################

import requests
from win10toast import ToastNotifier

def push_windows_notification(flag):
    toaster = ToastNotifier()
    # Set your notification message here
    NOTIFICATION_MESSAGE = "Visa appointments are available!"
    NOTIFICATION_MESSAGE_NO = "Visa appointments are not available!"
    if(flag == 'available'):
        toaster.show_toast("Visa Appointment Available!", NOTIFICATION_MESSAGE, duration=10)
    else:
        toaster.show_toast("Visa Appointment NOT Available!", NOTIFICATION_MESSAGE_NO, duration=10)


############################ API Request #######################################
import requests
import json
import datetime

url = "https://app.checkvisaslots.com/slots/v1"
api_keys = ['V9MAUL', 'DDDSTV', 'NU1PTZ', '6NMXQ1', '1WFAD9', 'OC14EC']
current_key_index = 0
payload = {}
headers = {
  'authority': 'app.checkvisaslots.com',
  'accept': '*/*',
  'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
  'dnt': '1',
  'extversion': '3.3.2',
  'origin': 'chrome-extension://beepaenfejnphdgnkmccjcfiieihhogl',
  'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'x-api-key': api_keys[current_key_index]
}

response = requests.request("GET", url, headers=headers, data=payload)
print('response => ', response.text)
json_resp = json.loads(response.text)
if("message" in json_resp and len(json_resp["message"])>0 ):
    print("API key limit reached!")
    current_key_index = (current_key_index + 1) % len(api_keys)
    headers["x-api-key"] = api_keys[current_key_index]
    response = requests.request("GET", url, headers=headers, data=payload)
    json_resp = json.loads(response.text)

if(json.loads(response.text)["slotDetails"][6]["slots"] == 0 and json.loads(response.text)["slotDetails"][7]["slots"] == 0):
    print(datetime.datetime.now(), "No appointments available", "Current key = "+headers["x-api-key"])
    # push_windows_notification('not available')
else:
    send_email()
    push_windows_notification('available')

exit()