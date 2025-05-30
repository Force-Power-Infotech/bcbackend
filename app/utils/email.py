from typing import List, Dict, Any, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_email(
    email_to: str, 
    subject: str, 
    html_content: str,
) -> bool:
    """
    Send email using configured email settings
    
    In production, replace this with your email service provider's API
    """
    try:
        # For development purposes, just log the email
        logger.info(f"Email would be sent to: {email_to}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Content: {html_content}")
        
        return True
        
        # In production, implement actual email sending:
        # message = MIMEMultipart()
        # message["From"] = settings.EMAILS_FROM_EMAIL
        # message["To"] = email_to
        # message["Subject"] = subject
        # message.attach(MIMEText(html_content, "html"))
        
        # with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        #     server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        #     server.sendmail(settings.EMAILS_FROM_EMAIL, email_to, message.as_string())
        # return True
    
    except Exception as e:
        logger.error(f"Failed to send email to {email_to}: {str(e)}")
        return False

def send_verification_email(email_to: str, username: str) -> bool:
    """
    Send an email verification email
    """
    subject = "Verify your BowlsAce account"
    html_content = f"""
    <html>
        <body>
            <h2>Welcome to BowlsAce!</h2>
            <p>Hi {username},</p>
            <p>Thank you for registering with BowlsAce. Your account has been created successfully.</p>
            <p>For now this is just a confirmation email. In production, this would contain a verification link.</p>
            <p>Best regards,<br>The BowlsAce Team</p>
        </body>
    </html>
    """
    
    return send_email(email_to=email_to, subject=subject, html_content=html_content)
