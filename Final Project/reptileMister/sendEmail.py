"""
Basic code used to send emails through external smtp server.
Tutorial here: 
https://bc-robotics.com/tutorials/sending-email-using-python-raspberry-pi/
"""

import smtplib

#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'ostrich.bagelwocreamcheese@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'Naglesbagels'  #change this to match your gmail password

class Emailer:
    def sendmail(self, recipient, subject, content):
         
        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
 
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
 
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
 
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit

"""
sender = Emailer()

sendTo = 'ostrich.bagelwocreamcheese@gmail.com'
emailSubject = "Hello World"
emailContent = "This is a test of the Emailer Class"
 
#Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
sender.sendmail(sendTo, emailSubject, emailContent)  
"""
