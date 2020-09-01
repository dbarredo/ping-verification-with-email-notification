import os
from datetime import datetime
from scapy.layers.inet import traceroute
import schedule
import time
import smtplib


sender = input('Sender Email : ')
password = input('password : ')
reciever = input('Receiver Email : ')
target_IP = input("Enter IP Address")


server_list = f"{target_IP}"



sender_email = f"{sender}"
password =  f"{password}" #create apppassword "https://myaccount.google.com/apppasswords"
rec_email = f"{reciever}"



def repeat():
   for ip in server_list:
       response = os.popen(f"ping {ip}").read()
       if "Received = 0" in response:
          print("-" * 50)
          print(f"Status: Down {ip} Ping Unsuccessful")
          print(str(datetime.now()))
          print("")
          traceroute(f'{ip}', maxttl=15)
          try:
             server = smtplib.SMTP('smtp.gmail.com', 587)
             server.ehlo()
             server.starttls()
             server.ehlo()
             server.login(sender_email, password)
             subject = f"[IP UNREACHABLE] : IP {ip}"
             body = f"Ping Status Monitor Unreachable for IP : {ip} "
             message = f"Subject: {subject}\n\n{body}"
             server.sendmail(sender_email, rec_email, message)
             print("-" * 50)
          except:
             print("Login Error to Mail Server")
       else:
          print("-" * 50)
          print(f"Status: Up {ip} Ping Successful")
          print("Date: " + str(datetime.now()))
          print("-" * 50)

repeat()

schedule.every(5).seconds.do(repeat)

while 1:
    schedule.run_pending()
    time.sleep(1)
