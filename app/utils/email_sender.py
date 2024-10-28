import sendgrid
from sendgrid.helpers.mail import *
import os

def sendgrid_send_email(recipients, subject, html_content, sender):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(sender)  # Change to your verified sender
        # Convert single email to list if necessary
        recipient_list = recipients if isinstance(recipients, list) else [recipients]
        to_emails = [To(email) for email in recipient_list]
        subject = subject
        html_content = Content("text/html", html_content)
        
        # Create mail with first recipient
        mail = Mail(
            from_email, 
            to_emails[0], 
            subject, 
            html_content
        )
        
        # Add additional recipients if any
        if len(to_emails) > 1:
            for to_email in to_emails[1:]:
                mail.add_to(to_email)
        
        response = sg.client.mail.send.post(request_body=mail.get())
        print('Email sent successfully!', response)
        return {"status": "Email sent successfully!"}
    except Exception as e:
        print('Error: ', e)
        return {"status": "Failed to send email"}
    
