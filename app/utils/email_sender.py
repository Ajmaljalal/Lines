import sendgrid
from sendgrid.helpers.mail import *
import os

def sendgrid_send_email(recipients, subject, html_content, sender):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(sender)  # Change to your verified sender
        to_email = To(recipients)  # Change to your recipient
        subject = subject
        html_content = Content("text/html", html_content)
        mail = Mail(from_email, to_email, subject, html_content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return {"status": "Email sent successfully!"}
    except Exception as e:
        print('Error: ', e)
        return {"status": "Failed to send email"}
    
