# email_utils/email_sender.py
"""
Module to handle sending emails.
"""

import os
import logging
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up logging
logger = logging.getLogger(__name__)

def send_email(sender_email, sender_password, recipient_email, subject, message, company_name, role, is_followup = False):
    """
    Sends an email with an attachment.
    
    Args:
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password.
        recipient_email (str): Recipient's email address.
        subject (str): Email subject.
        message (str): Email body message.
        company_name (str): Name of the company.
    """
    logger.info(f"Sending email to: {recipient_email}")

    resume_filename = "NeehaRathnaJanjanam_" + role.replace(" ", "") + "_Resume.pdf"
    resume_path = os.path.join("email_assets", resume_filename)

    success_log_file = f"{company_name}_successfully_sent_emails.txt"
    
    # Read the log file and see if the email already exists
    if not is_followup and os.path.exists(success_log_file):
        with open(success_log_file, 'r') as file:
            sent_emails = file.readlines()
        sent_emails = [email.strip() for email in sent_emails]
        if recipient_email in sent_emails:
            logger.info(f"Email already sent to {recipient_email}. Skipping...")
            return  # Exit the function if the email was already sent

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        # msg.attach(MIMEText(message, 'html')) - uncomment if you want your message to be formatted
        
        with open(resume_path, 'rb') as file:
            resume_attachment = MIMEApplication(file.read(), Name=resume_filename)
        resume_attachment['Content-Disposition'] = f'attachment; filename="{resume_filename}"'
        msg.attach(resume_attachment)
        
        server.sendmail(sender_email, recipient_email, msg.as_string())
        logger.info(f"Email sent successfully to {recipient_email}")

        # Log successfully sent email address to a text file
        with open(success_log_file, 'a') as file:
            file.write(recipient_email + '\n')

        server.quit()
    except Exception as e:
        logger.error("Error sending email:", exc_info=True)
        raise e
