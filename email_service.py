"""
Email OTP Service for Event Management System
Send OTP via Gmail SMTP (100% FREE)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()


class EmailOTPService:
    """Email OTP service for sending verification codes via Gmail"""
    
    def __init__(self):
        """Initialize email service with Gmail SMTP"""
        self.smtp_host = 'smtp.gmail.com'
        self.smtp_port = 587
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.enabled = bool(self.email_user and self.email_password)
        
        if self.enabled:
            print("✅ Email OTP service initialized successfully")
        else:
            print("⚠️ Email OTP service not configured")
    
    def generate_otp(self, length=6):
        """Generate a random OTP"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    def send_otp(self, email, otp, user_name="User", purpose="verification"):
        """
        Send OTP via email
        
        Args:
            email (str): Recipient email address
            otp (str): OTP code to send
            user_name (str): Name of the user
            purpose (str): Purpose of OTP (verification, login, etc.)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.enabled:
            return False, "Email service not configured"
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_user
            msg['To'] = email
            msg['Subject'] = f"🔐 Your Nexus Event OTP - {otp}"
            
            # HTML email body
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }}
                    .container {{ max-width: 600px; margin: 30px auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; color: white; }}
                    .header h1 {{ margin: 0; font-size: 28px; }}
                    .content {{ padding: 40px 30px; }}
                    .otp-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; margin: 30px 0; }}
                    .otp-code {{ font-size: 42px; font-weight: bold; letter-spacing: 10px; margin: 0; }}
                    .info {{ color: #666; line-height: 1.6; }}
                    .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #999; font-size: 12px; }}
                    .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; color: #856404; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Nexus Event Management</h1>
                        <p style="margin: 10px 0 0 0; opacity: 0.9;">Your OTP Verification Code</p>
                    </div>
                    
                    <div class="content">
                        <h2 style="color: #333;">Hello {user_name}!</h2>
                        <p class="info">We received a request for {purpose}. Your verification code is:</p>
                        
                        <div class="otp-box">
                            <p class="otp-code">{otp}</p>
                        </div>
                        
                        <div class="warning">
                            <strong>⏰ This OTP is valid for 10 minutes only.</strong>
                        </div>
                        
                        <p class="info">
                            <strong>Security Tips:</strong><br>
                            🔒 Never share this OTP with anyone<br>
                            🔒 Nexus Event will never ask for your OTP via phone or email<br>
                            🔒 If you didn't request this, please ignore this email
                        </p>
                        
                        <p class="info" style="margin-top: 30px;">
                            Best regards,<br>
                            <strong>Nexus Event Management Team</strong>
                        </p>
                    </div>
                    
                    <div class="footer">
                        <p>© 2025 Nexus Event Management. All rights reserved.</p>
                        <p>This is an automated email. Please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version
            text_body = f"""
            Hello {user_name}!
            
            Your OTP for {purpose} is: {otp}
            
            This OTP is valid for 10 minutes.
            
            Please do not share this OTP with anyone.
            
            Best regards,
            Nexus Event Management Team
            """
            
            # Attach both HTML and plain text
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            print(f"✅ Email OTP sent to {email}")
            return True, f"OTP sent successfully to {email}"
            
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def send_welcome_email(self, email, user_name):
        """Send welcome email to new users"""
        if not self.enabled:
            return False, "Email service not configured"
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_user
            msg['To'] = email
            msg['Subject'] = "🎉 Welcome to Nexus Event Management!"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }}
                    .container {{ max-width: 600px; margin: 30px auto; background: white; border-radius: 10px; overflow: hidden; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center; color: white; }}
                    .content {{ padding: 40px 30px; }}
                    .button {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎊 Welcome to Nexus Event!</h1>
                    </div>
                    <div class="content">
                        <h2>Hello {user_name}!</h2>
                        <p>Thank you for joining Nexus Event Management System.</p>
                        <p>You can now create and manage events, invite guests, and much more!</p>
                        <a href="http://localhost:5001/login" class="button">Login to Dashboard</a>
                        <p>Best regards,<br>Nexus Event Team</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            return True, "Welcome email sent"
            
        except Exception as e:
            return False, str(e)


# Initialize global service instance
email_otp_service = EmailOTPService()


# Testing
if __name__ == '__main__':
    print("🔧 Email OTP Service Testing")
    print("=" * 50)
    
    # Test OTP generation
    otp = email_otp_service.generate_otp()
    print(f"Generated OTP: {otp}")
    
    print("\n✅ Email OTP Service ready!")
    print("📝 Set EMAIL_USER and EMAIL_PASSWORD in .env file")
